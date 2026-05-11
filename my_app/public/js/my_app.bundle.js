

function patch_group_by_sidebar() {

	$(".group-by-item").each(function () {

		let $item = $(this);

		let email = decodeURIComponent(
			$item.attr("data-value") || ""
		);

		if (!email.includes("@")) {
			return;
		}

		let fullname =
			frappe.boot.user_info?.[email]?.fullname ||
			email;

		$item.find(".group-by-value").text(fullname);

	});

}

setInterval(() => {
	patch_group_by_sidebar();
}, 500);