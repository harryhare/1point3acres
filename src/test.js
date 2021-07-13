/* phantomjs test.js
 * 会报错
 * Fatal Windows exception, code 0xc0000005.
 * PhantomJS has crashed. Please read the bug reporting guide at
 * <http://phantomjs.org/bug-reporting.html> and file a bug report.
* */
var page = require('webpage').create();
page.open('https://www.1point3acres.com/bbs/', function (status) {
    console.log("Status: " + status);
    if (status === "success") {
        page.evaluate(function () {
            return null;
        });
        sleep(10);
        page.render('test.png');
    }
    phantom.exit();
});