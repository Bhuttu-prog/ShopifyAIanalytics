module Api
  module V1
    class HealthController < ApplicationController
      def check
        render json: { status: 'ok', service: 'Shopify Analytics API' }
      end
    end
  end
end

