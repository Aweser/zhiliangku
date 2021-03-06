module.exports = (function () {
  var func = {};
  func.goCourse = function (type, courseId, videoId) {
    switch (type * 1) {
      case 1:
      case 2:
        window.open('/tracks/video/detail/?course_id=' + courseId + '&video_id=' + videoId +'#/note')
        break;
      case 3:
        window.open('/tracks/live/detail/?course_id=' + courseId + '&video_id=' + videoId)
        break;
      case 4:
        window.open('/exercise/list/?course_id=' + courseId + '&video_id=' + videoId)
        break;
      default:
        break;
    }
  }
  func.showNotice=function(t,str,type){
      t.$notify({
        type: type||'info',
        message: str,
        offset: 100,
        duration: 3000,
        position: 'bottom-right'
      });
  }
  return func
})()
