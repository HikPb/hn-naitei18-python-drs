const csrftoken = Cookies.get('csrftoken');
class NotificationObj{
    constructor(notificationObj){
      this.notificationObj = notificationObj
      this.fromnow = moment(notificationObj.created_at).fromNow()

    }
    newRequestForm(){
      var reminder = `
        <a class="dropdown-item d-flex align-items-center" href="/drs/requestforms">
          <div class="mr-3">
            <div class="icon-circle bg-primary">
              <i class="fas fa-file-alt text-white"></i>
            </div>
          </div>
          <div>
            <div class="small text-gray-500">
            ${this.fromnow}
            </div>
            ${this.notificationObj.body}
          </div>
        </a>
      `
      return reminder;
    }
    responseRequest(){
      var reminder = `
        <a class="dropdown-item d-flex align-items-center" href="/drs/myforms/>
          <div class="mr-3">
            <div class="icon-circle bg-success">
              <i class="fas fa-donate text-white"></i>
            </div>
          </div>
          <div>
            <div class="small text-gray-500">
            ${this.fromnow}
            </div>
            ${this.notificationObj.body}
          </div>
        </a>
      `
      return reminder;
    }
    newReport(){
      var reminder = `
        <a class="dropdown-item d-flex align-items-center" href="/drs/requestforms">
          <div class="mr-3">
            <div class="icon-circle bg-warning">
              <i class="fas fa-exclamation-triangle text-white"></i>
            </div>
          </div>
          <div>
          <div class="small text-gray-500">
          ${this.fromnow}
          </div>
          ${this.notificationObj.content}
          </div>
        </a>
      `
      return reminder;
    }
    drawNotification(){
      if (this.notificationObj.type_notification == 'nr') return this.newRequestForm();
      if (this.notificationObj.type_notification == 'rr') return this.responseRequest();
      return this.newReport();
    }
  }

function loadNotifications(){
  $.ajax({
    method:'get',
    url:'/drs/ajax/get_notification_info',
    data:{},
    success: function(data){
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
    },
    error: function(data){
      console.log('ERR',data)
    }
  })
}

$('#alertsDropdown').click(function(){
  const tmpObjsHTML = $('#newNotifications').html()
  $.ajax({
    method:'post',
    url:"/drs/ajax/mark_notification_as_readed",
    data:{
      csrfmiddlewaretoken: csrftoken,
    },
    success:function(data){
      $('#newNotifications').html('')
      $('#cheat').html(tmpObjsHTML)
    },
    error:function(data){
      console.log('ERR',data)
    }
  })
})


window.setInterval(function(){
  loadNotifications();
}, 1000);
