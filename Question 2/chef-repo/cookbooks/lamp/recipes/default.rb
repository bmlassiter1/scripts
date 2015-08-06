#
# Cookbook Name:: lamp
# Recipe:: default
#
# Copyright 2015, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

execute "update-upgrade" do
  command "apt-get update && apt-get upgrade -y"
  action :run
end
