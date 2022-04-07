% include('head.tpl', title="Project list")
<div id="content" class="main_content">
<h2> Projects in the Fablab</h2>
% include('project_list.tpl', projects=projects)
</div>
% include('footer.tpl')