#!/usr/bin/env ruby
require 'bundler/setup'
require 'rack'
require 'rack/cors'
require 'json'
require 'httparty'
require 'dotenv/load'

class QuestionsController
  def self.create(env)
    request = Rack::Request.new(env)
    body = JSON.parse(request.body.read)
    
    question = body['question']
    store_id = body['store_id']
    
    unless question && store_id
      return [400, {'Content-Type' => 'application/json'}, [JSON.generate({
        error: 'validation_error',
        message: 'Question and store_id parameters are required'
      })]]
    end
    
    # Forward to Python AI service
    begin
      response = HTTParty.post(
        ENV.fetch('PYTHON_AI_SERVICE_URL', 'http://localhost:8000') + '/api/v1/analyze',
        body: {
          question: question,
          store_id: store_id
        }.to_json,
        headers: {
          'Content-Type' => 'application/json',
          'X-API-Key' => ENV.fetch('PYTHON_SERVICE_API_KEY', 'default-key')
        },
        timeout: 30
      )
      
      if response.success?
        [200, {'Content-Type' => 'application/json'}, [JSON.generate({
          answer: response['answer'],
          confidence: response['confidence'],
          query_used: response['query_used'],
          metadata: response['metadata']
        })]]
      else
        [500, {'Content-Type' => 'application/json'}, [JSON.generate({
          error: 'ai_service_error',
          message: 'Failed to get response from AI service'
        })]]
      end
    rescue => e
      [500, {'Content-Type' => 'application/json'}, [JSON.generate({
        error: 'internal_server_error',
        message: e.message
      })]]
    end
  end
end

class HealthController
  def self.check(env)
    [200, {'Content-Type' => 'application/json'}, [JSON.generate({
      status: 'ok',
      service: 'Shopify Analytics API'
    })]]
  end
end

app = Rack::Builder.new do
  use Rack::Cors do
    allow do
      origins '*'
      resource '*',
        headers: :any,
        methods: [:get, :post, :put, :patch, :delete, :options, :head]
    end
  end
  
  map '/api/v1/questions' do
    run lambda { |env|
      if env['REQUEST_METHOD'] == 'POST'
        QuestionsController.create(env)
      else
        [405, {'Content-Type' => 'application/json'}, [JSON.generate({error: 'Method not allowed'})]]
      end
    }
  end
  
  map '/api/v1/health' do
    run lambda { |env|
      HealthController.check(env)
    }
  end
  
  map '/' do
    run lambda { |env|
      [200, {'Content-Type' => 'text/plain'}, ['Shopify Analytics API - Use /api/v1/questions or /api/v1/health']]
    }
  end
end

run app

