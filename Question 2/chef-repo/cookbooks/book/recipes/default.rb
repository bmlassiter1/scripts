#
# Cookbook Name:: book
# Recipe:: default
#
# Copyright 2015, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

include_recipe 'test_site::apache'
include_recipe 'test_site::mysql'
include_recipe 'test_site::wordpress'

execute "update-upgrade" do
  command "apt-get update && apt-get upgrade -y"
  action :run
end
