<div id="entry_list">
% for entry in project['entries']:
	<div id= "entry_{{entry['id']}}" class="entry_list_elem list_elem"> 
		<span>Date started: {{entry['time_start']}}</span>
		<span>Date ended: {{entry['time_end']}}</span>
		<div id="entry_{{entry['id']}}_content" class="entry_list_elem_content">
			% for file in entry['files']:
				<div id="entry_{{entry['id']}}_file_{{file['name']">
					 % if file['type'] == 'bitmap':
					 	<img width ="300"src="/sudoc/repository/{{file['path']}}"/>
					 % else:
					 	<p>{{file['path']}}</p>
					 % end
				</div>
			% end
		</div>
	</div>
% end
</div>