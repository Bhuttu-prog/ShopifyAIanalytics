require 'httparty'
require 'openssl'

class ShopifyOAuthService
  include HTTParty
  
  def self.exchange_code_for_token(code, shop)
    response = HTTParty.post(
      "https://#{shop}/admin/oauth/access_token",
      body: {
        client_id: ENV['SHOPIFY_API_KEY'],
        client_secret: ENV['SHOPIFY_API_SECRET'],
        code: code
      },
      headers: {
        'Content-Type' => 'application/json'
      }
    )
    
    if response.success? && response['access_token']
      {
        success: true,
        access_token: response['access_token']
      }
    else
      {
        success: false,
        error: response['error'] || 'Failed to exchange code for token'
      }
    end
  rescue StandardError => e
    {
      success: false,
      error: e.message
    }
  end
  
  def self.verify_hmac(params, hmac)
    return false unless hmac.present?
    
    query_string = params.except(:hmac, :signature).sort.map { |k, v| "#{k}=#{v}" }.join('&')
    calculated_hmac = Base64.encode64(
      OpenSSL::HMAC.digest(
        OpenSSL::Digest.new('sha256'),
        ENV['SHOPIFY_API_SECRET'],
        query_string
      )
    ).strip
    
    calculated_hmac == hmac
  end
end

