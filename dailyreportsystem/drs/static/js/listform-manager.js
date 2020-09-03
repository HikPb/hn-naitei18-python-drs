function strtrunc(str, max, add){
    add = add || '...';
    return (typeof str === 'string' && str.length > max ? str.substring(0, max) + add : str);
 };
$(document).ready(
    function(){
        var table = $('#myforms').DataTable({
            "serverSide": true,
            "responsive": true,
            "order": [[ 3, "desc" ]],
            "ajax": {
                "url": "/api/allrequests/?format=datatables",
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
                {"data": "created_at"},
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
                {"data": "compensation_from"},
                {"data": "compensation_to"},
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
                    if(data['status'] == 'r' || data['status']== 'a'){
                        return '<button class="btn btn-info btn-detail" type="button">Detail</button>'
                                + '<button class="btn btn-secondary btn-approval" type="button" style="margin: 0px 3px;" disabled>Approval</button>'
                    }
                    return '<button class="btn btn-info btn-detail" type="button">Detail</button>'
                            + '<button class="btn btn-success btn-approval" type="button" style="margin: 0px 3px;">Approval</button>'
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
                            +"<td>Staff Code</td>"
                            +"<td>P123425</td>"
                        +"</tr>"
                        +"<tr>"
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
                            +"<td>Staff Code</td>"
                            +"<td>P123425</td>"
                        +"</tr>"
                        +"<tr>"
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
                            +"<td>Staff Code</td>"
                            +"<td>P123425</td>"
                        +"</tr>"
                        +"<tr>"
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
        $('#myforms tbody').on( 'click', '.btn-approval', function () {
            var data = table.row( $(this).parents('tr') ).data();
            action = "/drs/allforms/"+data['id']+"/update/"
            $('#approval').attr('action', action);
            $('#approval-modal').modal();
            
        } );
        $('body').on('hidden.bs.modal', '.modal', function () {
            $("#tb tbody").empty();
        });
    }
);
