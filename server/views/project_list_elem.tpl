<% 
	projectusers = []
	for user in project['users']:
		projectusers.append('<a href="/sudoc/user?id=%s">%s %s</a>'%(user['id'], user['firstname'], user['lastname']))
	end
	users = ', '.join(projectusers)
%>
<div class="project_list_elem_title"><a href= "/sudoc/project?id={{project['id']}}" >{{project['name']}}</a></div>
<div class="project_list_elem_infos">
	<p class="project_list_elem_infos_authors">Authors: {{!users}}</p>
	<p>Created: {{project['datecreated']}} Last Updated : {{project['dateupdated']}}</p>
	<p><a href="{{project['projecturl']}}">Documentation URL</a></p>
	<p>State : {{project['state']}}</p>
	<p>Type : {{project['type']}}</p>
</div>