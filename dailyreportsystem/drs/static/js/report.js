function strtrunc(str, max, add){
    add = add || '...';
    return (typeof str === 'string' && str.length > max ? str.substring(0, max) + add : str);
 };
$(document).ready(
    function(){
        var table = $('#listreport').DataTable({
            "serverSide": true,
            "responsive": true,
            "ajax": {
                "url": "/api/listreports/?format=datatables",
                "type": "GET",
                "beforeSend": function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token|escapejs }}");
                }
            },
            "columns": [
                {"data": "id"},
                {"data": "sender.name"},
                {"data": "created_at",
                "render": function(data, type, row){
                    return moment(data).format('HH:mm, DD-MM-YYYY')
                }},
                {"data": "plan.title"},
                {"data": "actual"},
                {"data": "issue"},
                {"data": "next",
                "visible": false,
                "searchable": false,},
                {"data": "receiver",
                "visible": false,
                "searchable": false,},
                {"data": null,
                'render': function(data, type, row, meta){
                    return '<button class="btn btn-info btn-detail" type="button"><i class="fa fa-eye"></i></button>'
                            + '<button class="btn btn-success btn-update" type="button" style="margin: 0px 3px;"><i class="fa fa-edit"></i></button>'
                            + '<button class="btn btn-danger btn-delete" type="button"><i class="fa fa-trash"></i></button>'
                    }
                },
            ],
            "columnDefs": [
                {
                    'targets': [4, 5],
                    'render': function(data, type, full, meta){
                        if(type === 'display'){
                            data = strtrunc(data, 60);
                        }
                    return data;
                    }
                }],
            "dom": 'Bfrtip',
            "buttons": [
                {
                    text: '<i class="fas fa-pen">Create</i>',
                    action: function ( e, dt, node, config ) {
                        window.location.replace("/drs/report/create")
                    }
                }
            ]
        });

        $('#listreport tbody').on( 'click', '.btn-detail', function () {
                var data = table.row( $(this).parents('tr') ).data();
                    $(".modal-body").find("#tb1 tbody")
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
                            +"<td>Plan</td>"
                            +"<td>"+data['plan']['title']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Actual</td>"
                            +"<td>"+data['actual']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Issue</td>"
                            +"<td>"+data['issue']+"</td>"
                        +"</tr>"
                        +"<tr>"
                            +"<td>Next</td>"
                            +"<td>"+data['next']+"</td>"
                        +"</tr>"
                        );
                $("#detail-modal").modal();
        } );
        $('#listreport tbody').on( 'click', '.btn-update', function () {
            var data = table.row( $(this).parents('tr') ).data();
            var urlParts = document.location.href.split("/");
            console.log(urlParts)
            location.replace("/drs/report/"+data['id']+"/update")
        } );
        $('#listreport tbody').on( 'click', '.btn-delete', function () {
            var data = table.row( $(this).parents('tr') ).data();
            // action = "{% url 'form_delete' "+data['id']+"%}"
            action = "/drs/report/"+data['id']+"/delete/"
            $('#delete').attr('action', action);
            $("#delete-confirm").modal()
        } );
        $('body').on('hidden.bs.modal', '.modal', function () {
            $("#tb1 tbody").empty();
        });
    }
)
