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
        constructor(position, radius) {
            super(position);
            this.radius = radius;
            this.color = new paper.Color(position.x/maxPosition.x, (maxPosition.x - position.x)/maxPosition.x, 0);
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

            this.color.red = this.position.x/maxPosition.x;
            this.color.green = (maxPosition.x - this.position.x)/maxPosition.x;
            this.circle.fillColor = this.color;
        }

        getPath() {
            return this.circle;
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
        new BallBlob(new paper.Point([0, 0]), maxPosition.x / 4.0, new paper.Color(0, 0.85, 0)),
        new BallBlob(new paper.Point([maxPosition.x, maxPosition.y]), maxPosition.x / 3.5, new paper.Color(1, 0, 0))
    ];

    var largeCircle = new Ball(ballBlobs[1].position, 50);
    var balls = [
        ballBlobs[0],
        ballBlobs[1],
        largeCircle
    ];

    var handle_len_rate = 2.4;
    var circlePaths = [];
    for (var i = 0, l = balls.length; i < l; i++) {
        circlePaths.push(balls[i].getPath());
    }


    // var connections = new paper.Group();
    // paper.project.activeLayer.appendTop(connections);
    //
    // function generateConnections(paths) {
    //     // Remove the last connection paths:
    //     connections.children = [];
    //
    //     for (var i = 0, l = paths.length; i < l; i++) {
    //         for (var j = i - 1; j >= 0; j--) {
    //             var path = metaball(paths[i], paths[j], 0.5, handle_len_rate, 300);
    //             if (path) {
    //                 connections.appendTop(path);
    //                 path.removeOnMove();
    //             }
    //         }
    //     }
    // }
    // generateConnections(circlePaths);

    paper.project.view.onFrame = function(event) {
        var oldX = largeCircle.position.x;
        var oldY = largeCircle.position.y;

        largeCircle.position.x = lerp(oldX, target.x, event.delta);
        largeCircle.position.y = lerp(oldY, target.y, event.delta);

        for (var i = 0; i < balls.length; i++) {
            balls[i].updatePath();
        }

        // generateConnections(circlePaths);
    };
    paper.project.view.onResize = function() {
        var newSize = paper.view.size;
        maxPosition = new paper.Point([newSize.width, newSize.height]);

        ballBlobs[0].radius = maxPosition.x / 4.0;
        ballBlobs[1].position = new paper.Point([maxPosition.x, maxPosition.y]);
        ballBlobs[1].radius = maxPosition.x / 3.5;

        console.log("maxPosition: [" + maxPosition.x + ", " + maxPosition.y + "]");
    };

    function metaball(ball1, ball2, v, handle_len_rate, maxDistance) {
        var center1 = ball1.position;
        var center2 = ball2.position;
        var radius1 = ball1.bounds.width / 2;
        var radius2 = ball2.bounds.width / 2;
        var pi2 = Math.PI / 2;
        var d = center1.getDistance(center2);
        var u1, u2;

        if (radius1 == 0 || radius2 == 0)
            return;

        if (d > maxDistance || d <= Math.abs(radius1 - radius2)) {
            return;
        } else if (d < radius1 + radius2) { // case circles are overlapping
            u1 = Math.acos((radius1 * radius1 + d * d - radius2 * radius2) /
                (2 * radius1 * d));
            u2 = Math.acos((radius2 * radius2 + d * d - radius1 * radius1) /
                (2 * radius2 * d));
        } else {
            u1 = 0;
            u2 = 0;
        }

        var angle1 = center2.subtract(center1).getAngleInRadians();
        var angle2 = Math.acos((radius1 - radius2) / d);
        var angle1a = angle1 + u1 + (angle2 - u1) * v;
        var angle1b = angle1 - u1 - (angle2 - u1) * v;
        var angle2a = angle1 + Math.PI - u2 - (Math.PI - u2 - angle2) * v;
        var angle2b = angle1 - Math.PI + u2 + (Math.PI - u2 - angle2) * v;
        var p1a = center1 + getVector(angle1a, radius1);
        var p1b = center1 + getVector(angle1b, radius1);
        var p2a = center2 + getVector(angle2a, radius2);
        var p2b = center2 + getVector(angle2b, radius2);

        // define handle length by the distance between
        // both ends of the curve to draw
        var totalRadius = (radius1 + radius2);
        var d2 = Math.min(v * handle_len_rate, (p1a - p2a).length / totalRadius);

        // case circles are overlapping:
        d2 *= Math.min(1, d * 2 / (radius1 + radius2));

        radius1 *= d2;
        radius2 *= d2;

        var path = new paper.Path({
            segments: [p1a, p2a, p2b, p1b],
            style: ball1.style,
            closed: true
        });
        var segments = path.segments;
        segments[0].handleOut = getVector(angle1a - pi2, radius1);
        segments[1].handleIn = getVector(angle2a + pi2, radius2);
        segments[2].handleOut = getVector(angle2b - pi2, radius2);
        segments[3].handleIn = getVector(angle1b + pi2, radius1);
        return path;
    }

    function getVector(radians, length) {
        return new paper.Point({
            // Convert radians to degrees:
            angle: radians * 180 / Math.PI,
            length: length
        });
    }
};

