% include('head.tpl', title=project['name'])
<div id="content" class="main_content">
<% 
	projectusers = []
	for user in project['users']:
		projectusers.append('<a href="/sudoc/user?id=%s">%s %s</a>'%(user['id'], user['firstname'], user['lastname']))
	end
	users = ', '.join(projectusers)
%>
<h2>{{project['name']}}</h2>
<span> <p> Authors: {{!users}} </p> <span>
<span>Created: {{project['datecreated']}}</span>
<span>Last Updated : {{project['dateupdated']}}</span>
<span>Documentation URL : {{project['projecturl']}}</span>
<span>State : {{project['state']}}</span>
<span>Type : {{project['type']}}</span>
% include('entry_list.tpl', project=project)
</div>
% include('footer.tpl')