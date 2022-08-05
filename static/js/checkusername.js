$('.username').bind('DOMNodeInserted DOMNodeRemoved',function () {       
    var username = $(this).val(); 
    console.log("...")       
    $.ajax({        
          url: '/check_username/',         
          data: {           
              'username': username          
          },         
          dataType: 'json',            
          success: function (data) {           
               if (data.username) {             
                  alert("Username already taken");
               }         
          }       
    });      
  });   
  
  setTimeout(function() {
        var username =  document.getElementById('username'); 
        console.log(username);    
        $.ajax({        
            url: '/check_username/',         
            data: {           
                'username': username          
            },         
            dataType: 'json',            
            success: function (data) {           
                if (data.username) {             
                    alert("Username already taken");
                }         
            }       
        });   
      }, 1000);
      
      $("body").on('DOMSubtreeModified', "username", function() {
        console.log("...");
        var username = $(this).val(); 
        $.ajax({        
                url: '/check_username/',         
                data: {           
                    'username': username          
                },         
                dataType: 'json',            
                success: function (data) {           
                    if (data.username) {             
                        alert("Username already taken");
                    }         
                }       
          });
        });