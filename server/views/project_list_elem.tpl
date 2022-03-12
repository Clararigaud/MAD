<% 
	projectusers = []
	for user in project['users']:
		projectusers.append('<a href="/sudoc/users/%s">%s %s</a>'%(user['id'], user['firstname'], user['lastname']))
	end
	users = ', '.join(projectusers)
%>
<span class="project_list_elem_title"><a href= "/sudoc/project?id={{project['id']}}" >{{project['name']}}</a></span>
<span>{{!users}}</span>
<span>Created: {{project['datecreated']}}</span>
<span>Last Updated : {{project['dateupdated']}}</span>
<span><a href="{{project['projecturl']}}">Documentation URL</a></span>
<span>State : {{project['state']}}</span>
<span>Type : {{project['type']}}</span>