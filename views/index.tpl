<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>HOMIE 2</title>

    <link href="lib/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">

    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <style>
        #loader {
          font-size: 5px;
          position: absolute;
          display: none;
          right: 20px;
          top: 20px;
          text-indent: -9999em;
          border-top: 1.1em solid rgba(0, 0, 0, 0.1);
          border-right: 1.1em solid rgba(0, 0, 0, 0.1);
          border-bottom: 1.1em solid rgba(0, 0, 0, 0.1);
          border-left: 1.1em solid rgba(0, 0, 0, 0.4);
          -webkit-transform: translateZ(0);
          -ms-transform: translateZ(0);
          transform: translateZ(0);
          -webkit-animation: load8 1.1s infinite linear;
          animation: load8 1.1s infinite linear;
        }
        #loader,
        #loader:after {
          border-radius: 50%;
          width: 6em;
          height: 6em;
        }
        @-webkit-keyframes load8 {
          0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
          }
          100% {
            -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
          }
        }
        @keyframes load8 {
          0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
          }
          100% {
            -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
          }
        }

    </style>
</head>
<body>

<div class="container theme-showcase" role="main">

    <div id="loader">Loading...</div>

    <section>
        <h2>All</h2>
        <div class="btn-group btn-group" role="group">
            <button type="button" class="btn btn-default" data-url="all/off">Off</button>
            <button type="button" class="btn btn-default" data-url="all/on">On</button>
        </div>

        <div class="btn-group btn-group" role="group">
            <button type="button" class="btn btn-default" data-url="dim/0">0</button>
            <button type="button" class="btn btn-default" data-url="dim/25">25</button>
            <button type="button" class="btn btn-default" data-url="dim/50">50</button>
            <button type="button" class="btn btn-default" data-url="dim/75">75</button>
            <button type="button" class="btn btn-default" data-url="dim/100">100</button>
        </div>
    </section>


    % for device in devices:
    <section>
        <h2>{{device.name}}</h2>

        <div class="btn-group btn-group-lg" role="group">
        % if device.model == 'selflearning-switch':
            <button type="button" class="btn btn-default" data-url="turn/{{device.id}}/off">Off</button>
            <button type="button" class="btn btn-default" data-url="turn/{{device.id}}/on">On</button>
        % elif device.model == 'selflearning-dimmer':
            <button type="button" class="btn btn-default" data-url="dim/{{device.id}}/0">0</button>
            <button type="button" class="btn btn-default" data-url="dim/{{device.id}}/25">25</button>
            <button type="button" class="btn btn-default" data-url="dim/{{device.id}}/50">50</button>
            <button type="button" class="btn btn-default" data-url="dim/{{device.id}}/75">75</button>
            <button type="button" class="btn btn-default" data-url="dim/{{device.id}}/100">100</button>
        % end
        </div>
    </section>
    % end

</div>

<script src="lib/jquery/dist/jquery.min.js"></script>
<script src="lib/fastclick/lib/fastclick.js"></script>
<script src="lib/bootstrap/dist/js/bootstrap.min.js"></script>
<script>
		$(function() {
			FastClick.attach(document.body);
		});

		$('button').click(function () {
			var $this = $(this);

			$('#loader').show();

			$.post($this.data('url'), function() {
				$('#loader').fadeOut();
			});
		});

</script>
</body>
</html>