function downloadPresentation(id) {
  var slideIds = getSlideIds(id);

  for (var i = 0, slideId; slideId = slideIds[i]; i++) {
    downloadSlide('Slide ' + (i + 1), id, slideId);
  }
}

function downloadSlide(name, presentationId, slideId) {
  var url = 'https://docs.google.com/presentation/d/' + presentationId +
    '/export/png?id=' + presentationId + '&pageid=' + slideId;
  var options = {
    headers: {
      Authorization: 'Bearer ' + ScriptApp.getOAuthToken()
    }
  };
  var response = UrlFetchApp.fetch(url, options);
  var image = response.getAs(MimeType.PNG);
  image.setName(name);
  DriveApp.createFile(image);
}

function getSlideIds(presentationId) {
  var url = 'https://slides.googleapis.com/v1/presentations/' + presentationId;
  var options = {
    headers: {
      Authorization: 'Bearer ' + ScriptApp.getOAuthToken()
    }
  };
  var response = UrlFetchApp.fetch(url, options);

  var slideData = JSON.parse(response);
  return slideData.slides.map(function(slide) {
    return slide.objectId;
  });
}

function start() {
  downloadPresentation('Slides document id')
}
