% include('head.tpl', title="Project list")
<div id="content" class="main_content">
<h1> Projects in the Fablab</h1>
% include('project_list.tpl', projects=projects)
</div>
% include('footer.tpl')