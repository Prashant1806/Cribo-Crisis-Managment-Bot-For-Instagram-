$(document).ready(function () {
  $("#chatbot-form").on("submit", function (e) {
    e.preventDefault();
    var user_input = $("#chatbot-input").val();
    $("#chatbot-input").val("");
    if (user_input !== "") {
      $("#chatbot-messages").append(
        '<div class="chatbot-message user-message">' +
          user_input +
          "</div>"
      );
      $("#chatbot-messages").append(
        '<div class="chatbot-message chatbot-loading-message">' +
          '<div class="spinner-border text-primary" role="status">' +
          '<span class="sr-only">Loading...</span>' +
          "</div>" +
          "</div>"
      );
      $.ajax({
        url: "/get_bot_response",
        type: "POST",
        data: JSON.stringify({ user_input: user_input }),
        contentType: "application/json",
        success: function (response) {
          $("#chatbot-messages").append(
            '<div class="chatbot-message chatbot-response-message">' +
              response +
              "</div>"
          );
          $("#chatbot-messages").animate(
            {
              scrollTop: $("#chatbot-messages").get(0).scrollHeight,
            },
            500
          );
        },
        error: function (xhr, status, error) {
          console.log("Error: " + error);
        },
      });
    }
  });
});
