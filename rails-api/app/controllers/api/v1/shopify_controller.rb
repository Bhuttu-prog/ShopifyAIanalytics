module Api
  module V1
    class ShopifyController < ApplicationController
      def oauth
        shop = params[:shop]
        return render json: { error: 'Shop parameter required' }, status: :bad_request unless shop.present?

        # Generate OAuth URL
        redirect_uri = "#{request.base_url}/api/v1/shopify/callback"
        scopes = 'read_orders,read_products,read_inventory'
        
        oauth_url = "https://#{shop}/admin/oauth/authorize?" \
                    "client_id=#{ENV['SHOPIFY_API_KEY']}&" \
                    "scope=#{scopes}&" \
                    "redirect_uri=#{CGI.escape(redirect_uri)}"
        
        render json: { oauth_url: oauth_url }
      end

      def callback
        code = params[:code]
        shop = params[:shop]
        
        if code.present? && shop.present?
          # Exchange code for access token
          token_response = ShopifyOAuthService.exchange_code_for_token(code, shop)
          
          if token_response[:success]
            render json: {
              message: 'Authentication successful',
              store_id: shop,
              access_token: token_response[:access_token]
            }
          else
            render json: {
              error: 'authentication_failed',
              message: token_response[:error]
            }, status: :unauthorized
          end
        else
          render json: {
            error: 'invalid_request',
            message: 'Missing code or shop parameter'
          }, status: :bad_request
        end
      end
    end
  end
end

