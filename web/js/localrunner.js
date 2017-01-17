RUN_LOCALLY_AFTER_MILLISECONDS = 2 * 1000;

// see: https://github.com/bshishov/CognitiveTestPlatform/blob/master/src/web/cognitive_tests/static/js/testRecorder.js
function LogRecorder() {
    var self = this;

    this.start = function(onstart) {
        self.startTime = Date.now();
        console.log(">>> START");
        onstart();
    }

    this.logEvent = function(eventName, args) {
        //console.log("Fake recorded event:", eventName, args);
    }

    this.send = function(complete, fail) {
        console.log(">>> SEND");
        complete();
    }

    this.getTime = function() {
        return Date.now() - self.startTime;
    }

    this.stop = function(onstop) {
        console.log(">>> STOP");
        onstop();
    }
}

function TestManager(recorder) {
    var element = document.createElement('div');
    var eventStart = new Event('start');
    var eventRecordingStop = new Event('recordingStop');
    var eventComplete = new Event('complete');
    var eventSendComplete = new Event('sendComplete');
    var eventSendFail = new Event('sendFail');
    var self = this;

    this.recorder = recorder;

    this.log = function(eventName, args) {
        this.recorder.logEvent(eventName, args);
        console.log("Test event:", eventName, args);
    }

    this.start = function() {
        recorder.start(function() {
            self.log("test_start");
            element.dispatchEvent(eventStart);
        });
    }

    this.complete = function() {
        self.log("test_complete");
        recorder.stop(function() {
            element.dispatchEvent(eventRecordingStop); // RECORDING STOPPED
            recorder.send(function() {
                element.dispatchEvent(eventSendComplete); // SEND COMPLETE
            }, function() {
                element.dispatchEvent(eventSendFail); // SEND FAIL
            });
        });
        element.dispatchEvent(eventComplete); // COMPLETE CALLED
        alert('LOCAL TEST COMPLETED')
    }

    this.on = function(eventName, callback) {
        element.addEventListener(eventName, callback);
    }

    this.getTime = function() {
        return this.recorder.getTime();
    }
}

function check_local() {
    console.log('Checking whether we should run locally');
    if (window.test === undefined) {
        console.log('Running locally');
        var test = new TestManager(new LogRecorder());
        document.dispatchEvent(CustomEvent('testInit',{'detail':{'test':test}}));

        var startButton = document.createElement('BUTTON');
        startButton.appendChild(document.createTextNode("START (LOCAL)"));
        startButton.onclick = function() {
            test.start();
        };
        document.body.appendChild(startButton);
    }
};

setTimeout(check_local, RUN_LOCALLY_AFTER_MILLISECONDS);