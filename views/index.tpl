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
        @-webkit-keyframes super-rainbow {
            0%   { background: #D9EDF7; }
            20%  { background: #D9F7EA; }
            40%  { background: #EBF7D9; }
            60%  { background: #F7E7D9; }
            80%  { background: #F7D9E6; }
            100% { background: #F0D9F7; }
        }

        @-moz-keyframes super-rainbow {
            0%   { background: #D9EDF7; }
            20%  { background: #D9F7EA; }
            40%  { background: #EBF7D9; }
            60%  { background: #F7E7D9; }
            80%  { background: #F7D9E6; }
            100% { background: #F0D9F7; }
        }

        button.working {
             -webkit-animation: super-rainbow 15s infinite alternate linear;
             -moz-animation: super-rainbow 15s infinite alternate linear;
        }
    </style>
</head>
<body>

<div class="container theme-showcase" role="main">

    <div id="status"></div>

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

            $this.addClass('working');
			//$('#status').text('Working..').show();

			$.post($this.data('url'), function() {
				//$('#status').fadeOut();
				$this.removeClass('working');
			});
		});

</script>
</body>
</html>