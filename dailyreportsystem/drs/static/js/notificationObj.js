class NotificationObj{
    constructor(notificationObj){
      this.notificationObj = notificationObj
    }
    newRequestForm(){
      var reminder = `
        <a class="dropdown-item d-flex align-items-center" href="{% url 'all_requests'%}">
          <div class="mr-3">
            <div class="icon-circle bg-primary">
              <i class="fas fa-file-alt text-white"></i>
            </div>
          </div>
          <div>
            <div class="small text-gray-500">
            moment(${this.notificationObj.created_at}).format('HH:mm DD-MM-YYYY')
            </div>
            ${this.notificationObj.body}
          </div>
        </a>
      `
      return reminder;
    }
    responseRequest(){
      var reminder = `
        <a class="dropdown-item d-flex align-items-center" href="{% url 'my_forms'%}">
          <div class="mr-3">
            <div class="icon-circle bg-success">
              <i class="fas fa-donate text-white"></i>
            </div>
          </div>
          <div>
            <div class="small text-gray-500">
            moment(${this.notificationObj.created_at}).format('HH:mm DD-MM-YYYY')
            </div>
            ${this.notificationObj.body}
          </div>
        </a>
      `
      return reminder;
    }
    newReport(){
      var reminder = `
        <a class="dropdown-item d-flex align-items-center" href="{% url 'manager_reports%}">
          <div class="mr-3">
            <div class="icon-circle bg-warning">
              <i class="fas fa-exclamation-triangle text-white"></i>
            </div>
          </div>
          <div>
          <div class="small text-gray-500">
          moment(${this.notificationObj.created_at}).format('HH:mm DD-MM-YYYY')
          </div>
          ${this.notificationObj.content}
          </div>
        </a>
      `
      return reminder;
    }
    drawNotification(){
      if (this.notificationObj.type == 'nr') return this.newRequestForm();
      if (this.notificationObj.type == 'rr') return this.responseRequest();
      return this.newReport();
    }
  }

  $('#alertsDropdown').click(function(){
    const tmpObjsHTML = $('#newNotifications').html()
    $.ajax({
      method:'post',
      url:'{% url "AJAXMarkNotificationAsReaded" %}',
      data:{
        csrfmiddlewaretoken:'{{csrf_token}}'
      },
      success:function(data){
        $('#newNotifications').html('')
        $('#cheat').html(tmpObjsHTML)
        $('#newNotificationCount').text(data.unreaded_notification_count)
      },
      error:function(data){
        console.log('ERR',data)
      }
    })
  })

  var ws = new WebSocket( 'ws://' + window.location.host + '/ws/notification/')

  ws.onopen = function(event){
    console.log('opened', event);
  }

  ws.onmessage = function(event){
    console.log('message', event);
    var data = JSON.parse(event.data);
    
    var old_notifications = JSON.parse(data.old_notifications);
    var unreaded_notifications = JSON.parse(data.unreaded_notifications);
    var unreaded_notification_count = data.unreaded_notification_count;

    $('#newNotifications').html('')
    unreaded_notifications.forEach(element => {
      var obj = new NotificationObj(element.fields)
      $('#newNotifications').append(obj.drawNotification())
    });

    $('#newNotificationCount').text(unreaded_notification_count)
    console.log('loaded')
  }

  ws.onclose = function(event){
    console.log('close', event);
  }

  ws.onerror = function(event){
    console.log('error', event);
  }

  // window.setInterval(function(){
  //   loadNotifications();
  // }, 1000);
