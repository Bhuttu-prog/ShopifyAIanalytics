Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      post 'questions', to: 'questions#create'
      get 'health', to: 'health#check'
      
      # Shopify OAuth endpoints
      get 'shopify/oauth', to: 'shopify#oauth'
      get 'shopify/callback', to: 'shopify#callback'
    end
  end
end

