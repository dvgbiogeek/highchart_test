angular.module('proteinApp', ['ngTable', 'ngSanitize'])
	// Factory gets the data from the url with the appropriate id
	.factory('AminoFactory', ['$http', function($http) {

		var base = '/protein/';
		var AminoFactory = {};

		AminoFactory.getComp = function(aminoId) {
			console.log(aminoId);
			return $http.get(base + aminoId);
		};

		return AminoFactory;
	}])

	.factory('ProteinListFactory', ['$http', function($http) {

		var protBase = '/api/v1/protein/';
		var glossBase = '/api/v1/glossary/';
		var ProteinListFactory = {};

		ProteinListFactory.getList = function() {
     	return $http.get(protBase);
		};
    ProteinListFactory.getGlossary = function() {
    	return $http.get(glossBase);
    };

    return ProteinListFactory;
   
	}])

	.controller('listController', ['$scope', 'ProteinListFactory', 
			function($scope, ProteinListFactory) {
		// console.log('controller');
		var proteinList;

		function getProteins() {
			ProteinListFactory.getList()
				.success(function(data) {
					$scope.proteinList = data.objects;
					console.log(data.objects);
				})
				.error(function() {
					console.log('retrieval of data failed');
				});
		}

		getProteins();
		
	}])

	.controller('GlossaryController', ['$scope', 'ProteinListFactory',
			function($scope, ProteinListFactory) {
		console.log('glossary');
		var glossary;

		function getGlossaryList() {
			ProteinListFactory.getGlossary()
				.success(function(data) {
					$scope.glossary = data.objects;
					console.log(data.objects);
				})
				.error(function() {
					console.log('error retrieving glossary terms');
				});
		}

		getGlossaryList();
		
	}])

	.controller('AminoController', ['$scope', 'AminoFactory', 
			function($scope, AminoFactory) {
		// Gets the protein id from the URL
		var currentUrl = window.location.href;
		var aminoId = currentUrl.split('/')[5];
		console.log(currentUrl, aminoId);

		this.details = {};
		this.proteinName = {};
		this.proteinData = {};
		this.structure = {};
		this.percent = {};

		// Calls the factory to retrive and store the data in the scope as details
		function getProteinData() {
			AminoFactory.getComp(aminoId)
				.success(function(data) {
					$scope.details = data.amino;
					$scope.proteinName = data.name;
					$scope.proteinData = data.protein;
					$scope.structure = data.secondary;
					$scope.percent = data.aminoPercent;
				})
				.error(function(error) {
					console.log('Unable to get data');
				});
		}

		getProteinData();

	}])

	.filter('markdown', ['$sce', function($sce) {
		var converter = new Showdown.converter();
		return function(value) {
			var html = converter.makeHtml(value || ''); 
			return $sce.trustAsHtml(html);
		};
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
						renderTo: document.getElementById('graph1'),
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false,
						height: 300
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
	}])

	.directive('percentBar', [function() {
		return {
			template: '<div id="container" style="margin: 0 auto">not working</div>',
			restrict: 'C',
			scope: {
				items: '='
			},
			// defines the chart in the view
			link: function(scope, element, attrs) {
				var chart = new Highcharts.Chart({
					chart: {
						renderTo: document.getElementById('graph3'),
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false,
						height: 300
					},
					title: {
						text: 'Amino Acid Percent'
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
					xAxis: {
						categories: function() {
							scope.items.forEach(function(arr) {
								arrValue.push(arr[0]);
							});
						}
					},
					yAxis: {
						title: 'percent of amino acid in protein'
					},
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
	}])
	.directive('structureBar', [function() {
		return {
			template: '<div id="container" style="margin: 0 auto">not working</div>',
			restrict: 'C',
			scope: {
				items: '='
			},
			// defines the chart in the view
			link: function(scope, element, attrs) {
				var chart = new Highcharts.Chart({
					chart: {
						renderTo: document.getElementById('graph2'),
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false,
						height: 300,
						width: 400
					},
					title: {
						text: 'Secondary Structure Fraction'
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
					xAxis: {
						categories: function() {
							scope.items.forEach(function(arr) {
								arrValue.push(arr[0]);
							});
						}
					},
					series: [{
						type: 'column',
						name: 'Secondary Structure',
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