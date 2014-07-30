function salvar_cliente() {
	path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
	var frm = $('#formCliente');
	console.log(path+frm.attr('action'));
	$.ajax({
    	url: path+frm.attr('action'),
        type: 'POST',
        dataType: 'json',
        data: frm.serialize(),
        success: function (data, textStatus, xhr) {
        	if(data.success == true){

                if (data.href != ''){
        		    //redirecionando para pagina data.href
        		    window.location.href = path + data.href;
                }
                else{
                    $('#modal_cliente').modal('hide');
                }
        	}
        	else
        	{
        		frm.html(data.html);
        		$('#html_contatos').html(data.html_contatos);
        	}
        },
        error : function(jqXHR, textStatus, errorThrown){
            alert('error: ' + textStatus + errorThrown);
        }
    });
}

function salvar_orcamento() {
	path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
	var frm = $('#formOrcamento');
	console.log(path+frm.attr('action'));
	$.ajax({
    	url: path+frm.attr('action'),
        type: 'POST',
        dataType: 'json',
        data: frm.serialize(),
        success: function (data, textStatus, xhr) {
        	if(data.success == true){

                //redirecionando para pagina data.href
                window.location.href = path + data.href;
        	}
        	else
        	{
        		frm.html(data.html);
        		$('#html_produtos').html(data.html_produtos);
        	}
        },
        error : function(jqXHR, textStatus, errorThrown){
            alert('error: ' + textStatus + errorThrown);
        }
    });
}


function rm_contato( index_contato ) {
	path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');

	$.ajax({
    	url: path+'/cliente/rm_contato/',
        type: 'POST',
        dataType: 'json',
        data: {index_contato:index_contato},
        success: function (response, textStatus, xhr) {
			$('#contatos').html(response.contatos);

        },
        error : function(jqXHR, textStatus, errorThrown){
            alert('error: ' + textStatus + errorThrown);
        }
    });
}

function add_contato() {

	var frm = $('#formContato');
    $.ajax({
    	url: frm.attr('action'),
        type: frm.attr('method'),
        dataType: 'json',
        data: frm.serialize(),
        success: function (response, textStatus, xhr) {

			$('#contatos').html(response.contatos);
			frm.html(response.formhtml);

        },
        error : function(jqXHR, textStatus, errorThrown){
            alert('error: ' + textStatus + errorThrown);
        }
    });
}

function rm_produto( produto_id ) {
	path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');

	$.ajax({
    	url: path+'/orcamento/rm_produto/',
        type: 'POST',
        dataType: 'json',
        data: {produto_id:produto_id},
        success: function (response, textStatus, xhr) {
			$('#produtos').html(response.produtos);
        },
        error : function(jqXHR, textStatus, errorThrown){
            alert('error: ' + textStatus + errorThrown);
        }
    });
}

function edit_produto( produto_id ) {
	path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');

	$.ajax({
    	url: path+'/orcamento/edit_produto/',
        type: 'POST',
        dataType: 'json',
        data: {produto_id:produto_id},
        success: function (response, textStatus, xhr) {
            $('#formItem').html(response.formhtml);
        },
        error : function(jqXHR, textStatus, errorThrown){
            alert('error: ' + textStatus + errorThrown);
        }
    });
}

function add_produto() {

	var frm = $('#formItem');
    $.ajax({
    	url: frm.attr('action'),
        type: frm.attr('method'),
        dataType: 'json',
        data: frm.serialize(),
        success: function (response, textStatus, xhr) {

			$('#produtos').html(response.produtos);
			frm.html(response.formhtml);

        },
        error : function(jqXHR, textStatus, errorThrown){
            alert('error: ' + textStatus + errorThrown);
        }
    });
}

function modal_consulta_cliente(){
    $('#modal_consulta_cliente').modal('show');
}

function select_cliente(id, nome){

    $('#cliente').val(id+' - '+nome);
    $('#modal_consulta_cliente').modal('hide');
}

function modal_consulta_produto(){
    $('#modal_consulta_produto').modal('show');
}

function select_produto(id, nome,valor){

    $('#produto').val(id+' - '+nome);
    $('#valor').val(valor);
    $('#modal_consulta_produto').modal('hide');
}

function consulta_produto (url) {
    $.ajax({
		url: path+"/produto/consulta_itens/"+url, // url
		type: 'POST',
		dataType: 'json',
		data: $('#form_consulta_produto').serialize(),

		success: function(data, textStatus, xhr) {

			$('#itens_consulta_produto').html( data.produtos );
		},
		error: function(xhr, textStatus, errorThrown) {
			//$('#cidade').html( '<option value="">Nenhuma cidade cadastrada para este estado</option>' );
		}
	});
}

function consulta_cliente (url) {

    $.ajax({
		url: path+"/cliente/consulta_itens/"+url, // url
		type: 'POST',
		dataType: 'json',
		data: $('#form_consulta_cliente').serialize(),

		success: function(data, textStatus, xhr) {

			$('#itens_consulta_cliente').html( data.clientes );
		},
		error: function(xhr, textStatus, errorThrown) {
			//$('#cidade').html( '<option value="">Nenhuma cidade cadastrada para este estado</option>' );
			}
		});

}

$(document).ready(function() {
    path = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
    $('#estado').change(function(){

		$.ajax({
		url: path+"/cidade/get_cidades/", // url
		type: 'POST',
		dataType: 'json',
		data: {estado: $(this).val()},
		beforeSend: function() {
			$("#cidade").html("<option value=''>Carregando...</option>");
		},
		success: function(data, textStatus, xhr) {

			var html = null;
			var cidade = data;

			html += '<option selected="selected" value="">Selecione uma Cidade</option>'
			$(cidade).each(function(key,val){
				html += '<option value="'+val.pk+'">'+val['fields']['nome']+'</option>';
			});
			$('#cidade').html( html );

		},
		error: function(xhr, textStatus, errorThrown) {
			$('#cidade').html( '<option value="">Nenhuma cidade cadastrada para este estado</option>' );
			}
		});
	});

    $('#submit_consulta_cliente').click(function(){
        consulta_cliente('');
    });

    $('#submit_consulta_produto').click(function(){
        consulta_produto('');
    });

});