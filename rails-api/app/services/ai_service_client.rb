require 'httparty'

class AiServiceClient
  include HTTParty
  
  base_uri ENV.fetch('PYTHON_AI_SERVICE_URL', 'http://localhost:8000')
  
  def self.ask_question(question, store_id)
    response = post('/api/v1/analyze', {
      body: {
        question: question,
        store_id: store_id
      }.to_json,
      headers: {
        'Content-Type' => 'application/json',
        'X-API-Key' => ENV.fetch('PYTHON_SERVICE_API_KEY', 'default-key')
      },
      timeout: 30
    })
    
    if response.success?
      {
        success: true,
        answer: response['answer'],
        confidence: response['confidence'],
        query_used: response['query_used'],
        metadata: response['metadata']
      }
    else
      {
        success: false,
        error: 'ai_service_error',
        message: response['error'] || 'Failed to get response from AI service'
      }
    end
  rescue HTTParty::Error => e
    Rails.logger.error("AI Service error: #{e.message}")
    {
      success: false,
      error: 'service_unavailable',
      message: 'AI service is currently unavailable'
    }
  rescue StandardError => e
    Rails.logger.error("Unexpected error: #{e.message}")
    {
      success: false,
      error: 'unexpected_error',
      message: e.message
    }
  end
end

