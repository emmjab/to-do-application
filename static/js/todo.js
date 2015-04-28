$(document).ready(function () {
	$(".done_box").click(function() {
		var data = {
			"id":this.id,
			"is_done":this.checked //this.checked
		}
		$.ajax({
			type: "POST",
			url: "/ajax_call",
			data: JSON.stringify(data),
			contentType: 'application/json;charset=UTF-8',
			success: function() {
				console.log("updated.")
				location.reload()
			}
		})
	})
})