/**
 * Created by mic on 2017/5/7.
 */

var number_format = function (num) {
    return (num.toFixed(2) + '').replace(/\d{1,3}(?=(\d{3})+(\.\d*)?$)/g, '$&,');
};

// 每月产品数变化趋势
var stuff_count_monthly = function (data_count, width) {
	var _width = width, _height = 400,
		_margins = {top: 50, left: 80, right: 50, bottom: 30};

	var dataset = data_count;

	var y_max = d3.max(dataset, function (d) {
		return d[1];
	});

	var svg = d3.select('.monthly-stats')
		.append('svg')
		.attr('width', _width)
		.attr('height', _height);

	var x_scale = d3.scale.ordinal()
		.domain(d3.range(dataset.length))
		.rangePoints([0, _width-_margins.left-_margins.right]);

	var y_scale = d3.scale.linear()
		.domain([0, y_max])
		.range([_height - _margins.bottom - _margins.top, 0]);

	var rScale = d3.scale.linear()
		.domain([0, d3.max(dataset, function(d) { return d[1]; })])
		.range([2, 5]);

	// 获取标题
	var _get_title = function () {
		return dataset[0][0] + '至' + dataset[dataset.length - 1][0] + '产品数趋势图';
	};

	svg.append('text')
		.text(_get_title())
		.attr('class', 'title')
		.attr('x', _width/4)
		.attr('y', 25)
		.attr('font-size', '18px');

	// 添加文本
	svg.selectAll('text.num')
		.data(dataset)
		.enter()
		.append('text')
		.attr('class', 'num')
		.text(function (d) {
			return d[1];
		})
		.attr('x', function (d, i) {
			return x_scale(i) + _margins.left - 20;
		})
		.attr('y', function (d) {
			return y_scale(d[1]) + _margins.top - 5;
		})
		.attr('font-size', '12px')
		.attr('fill', '#F36');

	// X轴网格线
	var x_inner = d3.svg.axis()
		.scale(x_scale)
		.tickSize(-_height+_margins.top+_margins.bottom, 0, 0)
		.tickFormat('')
		.orient('bottom')
		.ticks(dataset.length);

	var x_inner_bar = svg.append('g')
		.attr('class', 'inner_line')
		.attr('transform', 'translate('+ _margins.left +','+ (_height - _margins.bottom) +')')
		.call(x_inner);

	// y轴网格线
	var y_inner = d3.svg.axis()
		.scale(y_scale)
		.tickSize(-_width+_margins.right+_margins.left, 0, 0)
		.tickFormat('')
		.orient('left')
		.ticks(dataset.length);

	var y_inner_bar = svg.append('g')
		.attr('class', 'inner_line')
		.attr('transform', 'translate('+ _margins.left +', '+ _margins.top +')')
		.call(y_inner);



	// x轴
	var x_axis = d3.svg.axis()
		.scale(x_scale)
		.orient('bottom')
		.ticks(dataset.length);

	var x_bar = svg.append('g')
		.attr('class', 'x axis')
		.attr('transform', 'translate('+ _margins.left +','+ (_height - _margins.bottom) +')')
		.call(x_axis)
		.selectAll('text')
		.text(function (d) {
			return dataset[d][0];
		});
		//.attr('transform', "rotate(-45)");


	// y轴
	var y_axis = d3.svg.axis()
		.scale(y_scale)
		.orient('left')
		.ticks(10);
	var y_bar = svg.append('g')
		.attr('class', 'y axis')
		.attr('transform', 'translate('+ _margins.left +', '+ _margins.top +')')
		.call(y_axis)
		.append('text')
		.text('产品数（个）')
		.attr('transform', 'rotate(-90)')
		.attr('text-anchor', 'end')
		.attr('dy', '1.2em');

	// 添加折线
	var _line = d3.svg.line()
		.x(function (d, i) {
			return x_scale(i);
		})
		.y(function (d) {
			return y_scale(d[1]);
		})
		.interpolate('cardinal');

	var g = svg.append('g')
		.attr('class', 'linear')
		.attr('transform', 'translate('+ _margins.left+','+ _margins.top +')')
		.append('path')
		.attr('d', _line(dataset));

	// 添加圆点
	svg.selectAll('circle')
		.data(dataset)
		.enter()
		.append('circle')
		.attr('cx', function (d, i) {
			return x_scale(i) + _margins.left;
		})
		.attr('cy', function (d) {
			return y_scale(d[1]) + _margins.top;
		})
		.attr("r", function(d) {
			return 5;
			// return rScale(d[1]);
		})
		.attr('fill', '#F36');
};

// 客单价范围
var stuff_money_stats = function (dataset, width) {
	var _width = width, _height = 400, _rect_padding = 20;
		_margins = {top: 50, left: 30, right: 30, bottom: 30};

	var dataset = dataset;

	var y_max = d3.max(dataset, function (d) {
		return d[1];
	});

	var svg = d3.select('.money-stats')
		.append('svg')
		.attr('width', _width)
		.attr('height', _height);

	var x_scale = d3.scale.ordinal()
		.domain(d3.range(dataset.length))
		.rangeRoundBands([0, _width-_margins.left-_margins.right]);

	var y_scale = d3.scale.linear()
		.domain([0, y_max])
		.range([_height - _margins.bottom - _margins.top, 0]);

	// x轴
	var x_axis = d3.svg.axis()
		.scale(x_scale)
		.orient('bottom')
		.ticks(dataset.length);
	var x_bar = svg.append('g')
		.attr('class', 'x axis')
		.attr('transform', 'translate('+ _margins.left +','+ (_height - _margins.bottom) +')')
		.call(x_axis)
		.selectAll('text')
		.text(function (d) {
			var x_label = '';
			if (dataset[d][0] <= 100) {
				x_label += '<=';
			} else if (dataset[d][0] >= 3000) {
				x_label += '>=';
			} else {
				x_label += '';
			}
			x_label +=  dataset[d][0] + '元';
			return x_label;
		});
		//.attr("transform", "rotate(90)")


	// y轴
	var y_axis = d3.svg.axis()
		.scale(y_scale)
		.orient('left')
		.ticks(10);
	var y_bar = svg.append('g')
		.attr('class', 'y axis')
		.attr('transform', 'translate('+ _margins.left +', '+ _margins.top +')')
		.call(y_axis)
		.append('text')
		.text('产品数（个）')
		.attr('transform', 'rotate(-90)')
		.attr('text-anchor', 'end')
		.attr('dy', '1.2em');


	svg.selectAll('rect.money')
		.data(dataset)
		.enter()
		.append('rect')
		.attr('class', 'money')
		.attr('fill', '#F36')
		.attr('x', function (d, i) {
			return x_scale(i) + _rect_padding/2 + _margins.left;
		})
		.attr('y', function (d, i) {
			var min = y_scale.domain()[0];
			return y_scale(min) + _margins.top;
		})
		.attr('width', x_scale.rangeBand() - _rect_padding)
		.attr('height',function (d) {
			return 0;
		})
		.transition()
		.delay(function (d, i) {
			return i*200;
		})
		.duration(2000)
		.ease('bounce')
		.attr('y', function (d) {
			return y_scale(d[1]) + _margins.top;
		})
		.attr('height', function (d) {
			return _height - y_scale(d[1]) - _margins.bottom - _margins.top;
		});

	svg.selectAll('text.percent')
		.data(dataset)
		.enter()
		.append('text')
		.attr('class', 'percent')
		.attr('x', function (d, i) {
			return x_scale(i) + _margins.left + _rect_padding/2;
		})
		.attr('dx', function () {
			return (x_scale.rangeBand() - _rect_padding)/2;
		})
		.attr('dy', function (d) {
			return 20;
		})
		.text(function (d) {
			// 计算百分比
			var percent = Number(d[1])/d3.sum(dataset, function (d) {
					return d[1];
				})*100;
			// 保留一位小数点，末尾加一个百分号
			return percent.toFixed(1)+'%';
		})
		.attr('y', function (d) {
			var min = y_scale.domain()[0];
			return y_scale(min);
		})
		.transition()
		.delay(function (d, i) {
			return i * 200;
		})
		.duration(2000)
		.ease('bounce')
		.attr('y', function (d) {
			return y_scale(d[1]) + _margins.top - 30;
		});
};