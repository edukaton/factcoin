var startBallAnimation = function() {
    return new Promise(function(resolve, reject) {
        setTimeout(resolve, 100, 'foo');
    });
};

window.onload = function() {
    // Get a reference to the canvas object
    var canvas = document.getElementById('canvas-background');
    // Create an empty project and a view for the canvas:
    paper.setup(canvas);

    paper.project.currentStyle = {
        fillColor: 'black'
    };

    function lerp(v0, v1, t) {
        return (1 - t) * v0 + t * v1;
    }

    var maxPosition = new paper.Point([paper.view.size.width, paper.view.size.height]);
    var target = new paper.Point([0, 0]);

    class MovableEntity {
        constructor(position) {
            this.position = position.clone();
            this.point = new paper.Point(position.x, position.y);
        }

        updatePath() {
            this.point.x = this.position.x;
            this.point.y = this.position.y;
        }
    }

    class Ball extends MovableEntity {
        constructor(position, radius, color) {
            super(position);
            this.radius = radius;
            this.color = color;
            this.circle = new paper.Path.Circle({
                center: this.position,
                radius: this.radius,
                fillColor: this.color
            });
        }

        updatePath() {
            super.updatePath();
            this.circle.position = this.point;
            this.circle.radius = this.radius;
            this.circle.fillColor = this.color;
        }

        getPath() {
            return this.circle;
        }
    }

    class FlyingBall extends Ball {
        constructor(startingPosition, targetPosition, arriveCallback, radius, color) {
            super(startingPosition, radius, color);
            this.targetPosition = targetPosition;
            this.arriveCallback = arriveCallback;
        }

        updatePath(frameEvent) {
            var oldX = this.position.x;
            var oldY = this.position.y;

            this.position.x = lerp(oldX, this.targetPosition.x, frameEvent.delta);
            this.position.y = lerp(oldY, this.targetPosition.y, frameEvent.delta);

            super.updatePath();
            if (this.isFinished() && this.arriveCallback) {
                this.arriveCallback();
            }
        }

        isFinished() {
            return Math.abs(this.position.x - this.targetPosition.x) < 35
                && Math.abs(this.position.y - this.targetPosition.y) < 35;
        }

        deletePath() {
            this.circle.remove();
        }
    }

    class BallBlob extends MovableEntity {
        constructor(position, radius, color) {
            super(position);
            this.radius = radius;
            this.color = color;
            this.blob = new paper.Path.Circle({
                center: this.position,
                radius: this.radius,
                fillColor: this.color
            });
        }

        updatePath() {
            super.updatePath();
            this.blob.position = this.point;
            this.blob.radius = this.radius;
            this.blob.fillColor = this.color;
        }

        getPath() {
            return this.blob;
        }
    }

    var ballBlobs = [
        new BallBlob(new paper.Point([0, 0]), maxPosition.x / 4.0, new paper.Color('#CBCFD6')),
        new BallBlob(new paper.Point([maxPosition.x, maxPosition.y]), maxPosition.x / 3.5, new paper.Color('#F3E0AF'))
    ];

    var largeCircle = null;

    var allObjects = [
        ballBlobs[0],
        ballBlobs[1]
    ];

    var circlePaths = [];
    for (var i = 0, l = allObjects.length; i < l; i++) {
        circlePaths.push(allObjects[i].getPath());
    }

    paper.project.view.onFrame = function(frameEvent) {
        for (var i = 0; i < allObjects.length; i++) {
            allObjects[i].updatePath(frameEvent);
        }
        if (largeCircle) {
            largeCircle.updatePath(frameEvent);
        }
    };
    paper.project.view.onResize = function() {
        var newSize = paper.view.size;
        maxPosition = new paper.Point([newSize.width, newSize.height]);

        ballBlobs[0].radius = maxPosition.x / 4.0;
        ballBlobs[1].position = new paper.Point([maxPosition.x, maxPosition.y]);
        ballBlobs[1].radius = maxPosition.x / 3.5;

        console.log("maxPosition: [" + maxPosition.x + ", " + maxPosition.y + "]");
    };

    startBallAnimation = function () {
        return new Promise(function (resolve, reject) {
            if (!largeCircle) {
                largeCircle = new FlyingBall(ballBlobs[1].position, ballBlobs[0].position, resolve, 50, new paper.Color('#F3E0AF'));
            }
        }).then(() => {
            largeCircle.deletePath();
            largeCircle = null
        });
    }
};

