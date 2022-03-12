<div id="project_list">
% for project in projects:
	<div id= "project_{{project['id']}}" class="project_list_elem list_elem"> 
	% include('project_list_elem.tpl', project=project)
	</div>
% end
</div>