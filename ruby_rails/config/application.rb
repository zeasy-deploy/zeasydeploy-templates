require_relative "boot"

# Only load the frameworks we need (no ActiveRecord — no database for this template)
require "action_controller/railtie"
require "action_view/railtie"

module TemplateRails
  class Application < Rails::Application
    config.load_defaults 8.0
    config.api_only = true
  end
end
