(function() {
  var $block = $('#ward-councillor-search'),
      $btn = $block.find('.locate'),
      $form = $block.find('form.cllr');

  function foundLocation(position) {
    lat = position.coords.latitude;
    lng = position.coords.longitude;
    $form.find('[name=address]').val(lat + ',' + lng);
    $form.submit();
  }

  function noLocation() {
    $btn.text('Use your location');
    alert('Sorry, your browser was unable to determine your location.');
  }

  if ($block.length > 0) {
    // setup ward councillor widget on homepage
    $btn.on('click', function(e) {
      e.preventDefault();
      $btn.text('Locating...');
      navigator.geolocation.getCurrentPosition(foundLocation, noLocation, {timeout:10000});
    });
  }
})();

$(document).on('scroll', function() {
  $(".navbar").toggleClass("scrolled", $(document).scrollTop() >= 60);
});
