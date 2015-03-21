angular.module('proteinApp', [])
	// Factory gets the data from the url with the appropriate id
	.factory('AminoFactory', ['$http', function($http) {

		var base = '/protein/';
		var AminoFactory = {};

		AminoFactory.getComp = function(aminoId) {
			return $http.get(base + aminoId);
		};

		return AminoFactory;
	}])

	.controller('AminoController', ['$scope', 'AminoFactory', 
			function($scope, AminoFactory) {
		// Gets the protein id from the URL
		var currentUrl = window.location.href;
		var aminoId = currentUrl.split('/')[4];

		this.details = {};
		this.proteinName = {};

		// Calls the factory to retrive and store the data in the scope as details
		function getProteinData() {
			AminoFactory.getComp(aminoId)
				.success(function(data) {
					$scope.details = data.amino;
					$scope.proteinName = data.name;
				})
				.error(function(error) {
					console.log('Unable to get data');
				});
		}

		getProteinData();
	}])

	.directive('aminoBar', [function() {
		return {
			// if the chart does not appear the template says 'not working'
			template: '<div id="container" style="margin: 0 auto">not working</div>',
			// use the directive as a class (<div class="hc-bar">) within the template - based on restrict
			restrict: 'C',
			// the values passed in to the directive are treated as a JSON object - any changes in the parent scope will be made available to the directive.
			scope: {
				// "items" is an attribute in the HTML in the same div as the chart
				items: '='
			},
			// defines the chart in the view
			link: function(scope, element, attrs) {
				var chart = new Highcharts.Chart({
					chart: {
						renderTo: document.getElementById('graph'),
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false,
					},
					title: {
						text: 'Amino Acid Composition'
					},
					tooltip: {
						enabled: false
					},
					plotOptions: {
						column: {
							dataLabels: {
								enabled: true,
								color: '#000000',
								connectColor: '#000000',
								formatter: function() {
									return '<b>' + this.y + ' </b>';
								}
							}
						}
					},
					// Takes the first value of each object in the array and uses it for the categories on the x-axis
					xAxis: {
						categories: function() {
							scope.items.forEach(function(arr) {
								arrValue.push(arr[0]);
							});
						}
					},
					yAxis: {
						title: 'quantity of amino acid in protein'
					},
					// uses the 2nd value of each object in the array for the data
					series: [{
						type: 'column',
						name: 'Amino Acids',
						data: function() {
							scope.items.forEach(function(arr) {
								arrValue.push(arr[1]);
							});
						}
					}]
				});

				scope.$watch('items', function(newValue) {
					chart.series[0].setData(newValue, true);
				});
			}
		};
	}]);