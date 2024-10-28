#!/usr/bin/env ruby

require 'dotenv'
require 'net-imap'

Dotenv.load('.env')


smtp_host = ENV['ROADSTEAD_SMTP_HOST']
mail_user = ENV['ROADSTEAD_EMAIL_USER']
email_password = ENV['ROADSTEAD_EMAIL_PASSWORD']

imap = Net::IMAP.new(smtp_host, 587, :ssl => true)
imap.port => 993
imap.tls_verified? => true

case imap.greeting.name
in /OK/i
  imap.authenticate("PLAIN", mail_user, email_password)
in  /PREAUTH/i
end

