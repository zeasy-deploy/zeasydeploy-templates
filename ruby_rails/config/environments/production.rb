require "active_support/core_ext/integer/time"

Rails.application.configure do
  config.eager_load = true
  config.consider_all_requests_local = false
  config.secret_key_base = ENV["SECRET_KEY_BASE"] || "placeholder_secret_key_base_for_template_testing_only"
end
