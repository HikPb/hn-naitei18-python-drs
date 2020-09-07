function strtrunc(str, max, add){
    add = add || '...';
    return (typeof str === 'string' && str.length > max ? str.substring(0, max) + add : str);
 };
$(document).ready(
    function(){
        var table = $('#myforms').DataTable({
            "serverSide": true,
            "responsive": true,
            "pageLength": 5,
            "ajax": {
                "url": "/api/myforms/?format=datatables",
                "type": "GET",
                "beforeSend": function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token|escapejs }}");
                }
            },
            "columns": [
                {"data": "id"},
                {"data": "title"},
                {"data": "form_type",
                'render': function(data, type, row){
                    if(data == 'il'){
                        return `<span style="font-size: 18px">In Late</span>`
                    }
                    if(data == 'lo'){
                        return `<span style="font-size: 18px">Leave Out</span>`
                    }
                    if(data == 'le'){
                        return `<span style="font-size: 18px">Leave Early</span>`
                    }
                }},
                {"data": "created_at",
                "render": function(data, type, row){
                    return moment(data).format('HH:mm DD-MM-YYYY')
                }},
                {"data": "checkin_time",
                "visible": false,
                "searchable": false,},
                {"data": "checkout_time",
                "visible": false,
                "searchable": false,},
                {"data": "leave_from",
                "visible": false,
                "searchable": false,},
                {"data": "leave_to",
                "visible": false,
                "searchable": false,},
                {"data": "compensation_from",
                "render": function(data, type, row){
                    return moment(data).format('HH:mm DD-MM-YYYY')
                }},
                {"data": "compensation_to",
                "render": function(data, type, row){
                    return moment(data).format('HH:mm DD-MM-YYYY')
                }},
                {"data": "content"},
                {"data": "status",
                'render': function(data, type, row){
                    if(data == 'p'){
                        return '<span class="badge badge-primary">Pending</span>'
                    }
                    if(data == 'c'){
                        return '<span class="badge badge-warning">Canceled</span>'
                    }
                    if(data == 'f'){
                        return '<span class="badge badge-default">Forwarded</span>'
                    }
                    if(data == 'r'){
                        return '<span class="badge badge-danger">Rejected</span>'
                    }
                    if(data == 'a'){
                        return '<span class="badge badge-success">Approved</span>'
                    }
                }},
                {"data": "sender",
                "visible": false,
                "searchable": false,},
                {"data": "receiver",
                "visible": false,
                "searchable": false,},
                {"data": null, 
                'render': function(data, type, row, meta){
                    if(data['status'] != 'p'){
                        return '<button class="btn btn-info btn-detail" type="button"><i class="fa fa-eye"></i></button>'
                        + '<button class="btn btn-success btn-update" type="button" style="margin: 0px 3px;" disabled><i class="fa fa-edit"></i></button>'
                        + '<button class="btn btn-danger btn-delete" type="button" disabled><i class="fa fa-trash"></i></button>'
                    }
                    return '<button class="btn btn-info btn-detail" type="button"><i class="fa fa-eye"></i></button>'
                            + '<button class="btn btn-success btn-update" type="button" style="margin: 0px 3px;"><i class="fa fa-edit"></i></button>'
                            + '<button class="btn btn-danger btn-delete" type="button"><i class="fa fa-trash"></i></button>'
                    }
                },               
            ],
            "columnDefs": [
                {
                    'targets': [1, 10],
                    'render': function(data, type, full, meta){
                        if(type === 'display'){
                            data = strtrunc(data, 30);
                        }
                    return data;
                    }
                }],
            "dom": 'Bfrtip',
            "buttons": [
                {
                    text: 'Create',
                    action: function ( e, dt, node, config ) {
                        window.location.replace("/drs/requestform/create")
                    }
                }
            ]
        });
        $('#myforms tbody').on( 'click', '.btn-detail', function () {
                var data = table.row( $(this).parents('tr') ).data();
                var temp;
                if(data['status'] == 'p'){
                    temp = '<span class="badge badge-primary">Pending</span>'
                }
                if(data['status'] == 'c'){
                    temp = '<span class="badge badge-warning">Canceled</span>'
                }
                if(data['status'] == 'f'){
                    temp = '<span class="badge badge-default">Forwarded</span>'
                }
                if(data['status'] == 'r'){
                    temp = '<span class="badge badge-danger">Rejected</span>'
                }
                if(data['status'] == 'a'){
                    temp = '<span class="badge badge-success">Approved</span>'
                }

                if(data['form_type']=="il"){
                    $(".modal-body").find("#tb tbody")
                    .append(
                        "<tr>"
                            +"<td>Employee name</td>"
                            +"<td>"+data['sender']['name']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Receiver</td>"
                            +"<td>"+data['receiver']['name']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Created at</td>"
                            +"<td>"+moment(data['created_at']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Checkin</td>"
                            +"<td>"+moment(data['checkin_time']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Compensation</td>"
                            +"<td>"+moment(data['compensation_from']).format('HH:mm')+" - "+moment(data['compensation_to']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Form type</td>"
                            +"<td>In Late</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Status</td>"
                            +"<td>"+temp+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Reason</td>"
                            +"<td>"+data['content']+"</td>"
                        +"</tr>"
                        );
                }
                
                if(data['form_type']=="le"){
                    $(".modal-body").find("#tb tbody")
                    .append(
                        "<tr>"
                            +"<td>Employee name</td>"
                            +"<td>"+data['sender']['name']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Receiver</td>"
                            +"<td>"+data['receiver']['name']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Created at</td>"
                            +"<td>"+moment(data['created_at']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Check out</td>"
                            +"<td>"+moment(data['checkout_time']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Compensation</td>"
                            +"<td>"+moment(data['compensation_from']).format('HH:mm')+" - "+moment(data['compensation_to']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Form type</td>"
                            +"<td>Leave Early</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Status</td>"
                            +"<td>"+temp+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Reason</td>"
                            +"<td>"+data['content']+"</td>"
                        +"</tr>"
                        );
                }

                if(data['form_type']=="lo"){
                    $(".modal-body").find("#tb tbody")
                    .append(
                        "<tr>"
                            +"<td>Employee name</td>"
                            +"<td>"+data['sender']['name']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Receiver</td>"
                            +"<td>"+data['receiver']['name']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Created at</td>"
                            +"<td>"+data['created_at']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Leave</td>"
                            +"<td>"+moment(data['leave_from']).format('HH:mm')+" - "+moment(data['leave_to']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Compensation</td>"
                            +"<td>"+moment(data['compensation_from']).format('HH:mm')+" - "+moment(data['compensation_to']).format('HH:mm, DD-MM-YYYY')+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Form type</td>"
                            +"<td>Leave Out</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Status</td>"
                            +"<td>"+temp+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Reason</td>"
                            +"<td>"+data['content']+"</td>"
                        +"</tr>"
                        );
                }
                $("#detail-modal").modal();
        } );
        $('#myforms tbody').on( 'click', '.btn-update', function () {
            var data = table.row( $(this).parents('tr') ).data();
            var urlParts = document.location.href.split("/");
            console.log(urlParts)
            location.replace("/drs/requestform/"+data['id']+"/update")
        } );
        $('#myforms tbody').on( 'click', '.btn-delete', function () {
            var data = table.row( $(this).parents('tr') ).data();
            action = "/drs/requestform/"+data['id']+"/delete/"
            $('#delete').click(function(){
                $.ajax({
                    url: action,
                    type: "POST",
                    data: { 'pk' : data['id'] },
                    success: function(data){
                        if(data.form_is_valid){
                            $("#delete-confirm").modal('hide')
                            table.ajax.reload();
                        }
                    }       
                });
            })
            $("#delete-confirm").modal()
        } );
        $('body').on('hidden.bs.modal', '.modal', function () {
            $("#tb tbody").empty();
        });
    }
);
