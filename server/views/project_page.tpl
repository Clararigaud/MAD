% include('head.tpl', title=project['name'])
<div id="content" class="main_content">
<% 
	projectusers = []
	for user in project['users']:
		projectusers.append('<a href="/sudoc/users/%s">%s %s</a>'%(user['id'], user['firstname'], user['lastname']))
	end
	users = ', '.join(projectusers)
%>
<h1>{{project['name']}}</h1>
<span> <p> Authors: {{!users}} </p> <span>
<span>Created: {{project['datecreated']}}</span>
<span>Last Updated : {{project['dateupdated']}}</span>
<span>Documentation URL : {{project['projecturl']}}</span>
<span>State : {{project['state']}}</span>
<span>Type : {{project['type']}}</span>
% include('entry_list.tpl', project=project)
</div>
% include('footer.tpl')