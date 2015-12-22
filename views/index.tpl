<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, user-scalable=no">
	<meta name="apple-mobile-web-app-capable" content="yes">
	<title>HOMIE 2</title>
    <link href="lib/normalize-css/normalize.css" rel="stylesheet" type="text/css" />
	<style>
		body, button {
			font-size: 20px;
            line-height: 1em;
		}
		button {
			margin-right: 2px;
            padding: 0px;
		}
		#status {
			position: absolute;
			top: 0;
			right: 0;
			padding: 10px;
			background: #fff;
			font-family: sans-serif;
		}
        form {
            display: inline-block;
        }
        section {
            padding: 10px;
            clear: both;
        }
        hr {
            clear: both;
        }
        h2 {
            margin: 10px 0 5px;
        }
	</style>
</head>
<body>

	<div id="status"></div>

    <section>
        <h2>All</h2>

        <form action="all/off" method="post">
            <button type="submit">Off</button>
        </form>

        <form action="all/on" method="post">
            <button type="submit">On</button>
        </form>
    </section>
    <section>
        <form action="dim/0" method="post">
            <button type="submit">0</button>
        </form>

        <form action="dim/25" method="post">
            <button type="submit">25</button>
        </form>

        <form action="dim/50" method="post">
            <button type="submit">50</button>
        </form>

        <form action="dim/75" method="post">
            <button type="submit">75</button>
        </form>

        <form action="dim/100" method="post">
            <button type="submit">100</button>
        </form>
    </section>


    % for device in devices:
    <section>
        <h2>{{device.name}}</h2>

        <form action="dim/taklampor/0" method="post">
            <button type="submit">0</button>
        </form>

        <form action="dim/taklampor/25" method="post">
            <button type="submit">25</button>
        </form>

        <form action="dim/taklampor/50" method="post">
            <button type="submit">50</button>
        </form>

        <form action="dim/taklampor/75" method="post">
            <button type="submit">75</button>
        </form>

        <form action="dim/taklampor/100" method="post">
            <button type="submit">100</button>
        </form>
    </section>
    % end


    <section>
        <h2>Byrå</h2>

        <form action="dim/byra/0" method="post">
            <button type="submit">0</button>
        </form>

        <form action="dim/byra/25" method="post">
            <button type="submit">25</button>
        </form>

        <form action="dim/byra/50" method="post">
            <button type="submit">50</button>
        </form>

        <form action="dim/byra/75" method="post">
            <button type="submit">75</button>
        </form>

        <form action="dim/byra/100" method="post">
            <button type="submit">100</button>
        </form>
    </section>


    <section>
        <h2>Bordslampor</h2>

        <form action="turn/bordslampor/off" method="post">
            <button type="submit">Off</button>
        </form>

        <form action="turn/bordslampor/on" method="post">
            <button type="submit">On</button>
        </form>
    </section>


	<script src="lib/jquery/dist/jquery.min.js"></script>
	<script src="lib/fastclick/lib/fastclick.js"></script>
	<script>
		$(function() {
			FastClick.attach(document.body);
		});

		$('form').submit(function () {
			var $this = $(this);

			$('#status').text('Working..').show();

			$.post($this.attr('action'), function() {
				$('#status').fadeOut();
			});

			return false;
		});
	</script>
</body>
</html>