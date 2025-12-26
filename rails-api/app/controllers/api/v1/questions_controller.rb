module Api
  module V1
    class QuestionsController < ApplicationController
      before_action :validate_request

      def create
        question = params[:question]
        store_id = params[:store_id]
        
        # Log the request
        Rails.logger.info("Received question: #{question} for store: #{store_id}")
        
        # Forward to Python AI service
        response = AiServiceClient.ask_question(question, store_id)
        
        if response[:success]
          render json: {
            answer: response[:answer],
            confidence: response[:confidence],
            query_used: response[:query_used],
            metadata: response[:metadata]
          }, status: :ok
        else
          render json: {
            error: response[:error],
            message: response[:message]
          }, status: :unprocessable_entity
        end
      rescue StandardError => e
        Rails.logger.error("Error processing question: #{e.message}")
        Rails.logger.error(e.backtrace.join("\n"))
        
        render json: {
          error: 'internal_server_error',
          message: 'An error occurred while processing your question'
        }, status: :internal_server_error
      end

      private

      def validate_request
        unless params[:question].present?
          render json: {
            error: 'validation_error',
            message: 'Question parameter is required'
          }, status: :bad_request
          return
        end

        unless params[:store_id].present?
          render json: {
            error: 'validation_error',
            message: 'Store ID parameter is required'
          }, status: :bad_request
          return
        end
      end
    end
  end
end

