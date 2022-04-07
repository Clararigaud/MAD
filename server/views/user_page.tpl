% include('head.tpl', title="{{ }}")
<div id="content" class="main_content">
<h2> {{user['prenom']+' '+user['nom']}}</h2>
<div id="user_infos">
	<p>Email: {{user['mail']}}</p>
	<p>Type: {{user['type']}}</p>
	<p>Commentaires: {{user['commentaires']}}</p>
</div>
% include('project_list.tpl', projects=projects)
</div>
% include('footer.tpl')