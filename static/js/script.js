window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

document.querySelectorAll(".deleteVenueBtn").forEach((el) => {
  el.addEventListener("click", function (e) {
    const venueId = this.getAttribute("data-id");

    fetch(`/venues/${venueId}`, { method: "DELETE" }).finally(() => {
      window.location.href = "/";
    });
  });
});
