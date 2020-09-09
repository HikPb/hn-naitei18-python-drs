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
                "url": "/api/managerlistreports/?format=datatables",
                "type": "GET",
                "beforeSend": function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token|escapejs }}");
                }
            },
            "columns": [
                {"data": "id"},
                {"data": "sender",
                "render": function(data, type, row){
                    return data['name']
                }},
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
                    return '<button class="btn btn-info btn-detail" type="button"><i class="fa fa-eye"></i></button>'},
                }
            ],
            "columnDefs": [
                {
                    'targets': [4, 5],
                    'render': function(data, type, full, meta){
                        if(type === 'display'){
                            data = strtrunc(data, 30);
                        }
                    return data;
                    }
                }],
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
                            +"<td>"+data['plan']+"</td>"
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
        $('body').on('hidden.bs.modal', '.modal', function () {
            $("#tb1 tbody").empty();
        });
    }
);
