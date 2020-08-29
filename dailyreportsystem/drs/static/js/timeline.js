// loadOnScroll handler
var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if ($(window).scrollTop() > $(document).height() - ($(window).height()*3)) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).unbind();
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        loadItems();
    }
};

var loadItems = function() {
    // If the next page doesn't exist, just quit now 
    if (hasNextPage == false) {
        return false
    }
    // Update the page number
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    var url = "/drs/ajax/timeline/" + pageNum + '/';
    $.ajax({
        url: url, 
        dataType: 'json',
        success: function(response) {
            // Update global next page variable
            var data = response.object_list;
            hasNextPage = response.hasNext;
            // Loop through all items
            var html = [];
            data.forEach(item => {
              var tl_content = ""
              item.events.forEach(e =>{
                tl_content += `<div class="box-item">
                                <span style="margin-right: 10px;">` +e.time+ `</span><strong style="margin-right: 10px;">`+e.event+`</strong><span>`+e.content+`</span>
                              </div>`
              })
              html.push(
                `<div class="timeline-section">
                  <div class="col-sm-12">
                    <div class="timeline-box">
                      <div class="box-title">
                        <span class="timeline-date">`
                          +item.date+
                        `</span>
                      </div>
                      <div class="box-content">`
                        +tl_content+
                      `</div>
                    </div>
                  </div>
                </div>`)
            });
            // Pop all our items out into the page
            $("#timeline-anchor").before(html.join(""));
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);
        }
    });
};

$(document).ready(function(){     
   $(window).bind('scroll', loadOnScroll);
});
