/**
 * Created by mic on 2017/4/20.
 */

// var format = d3.format(".1%");//设置刻度的格式
// 定义X轴
// var xAxis = d3.svg.axis()
//	.scale(xScale)
//	.ticks(5)//最多刻度数，连上原点
//	.orient("bottom")
//	.tickFormat(format);//添加刻度格式
var number_format = function (num) {
    return (num.toFixed(2) + '').replace(/\d{1,3}(?=(\d{3})+(\.\d*)?$)/g, '$&,');
};

// 24小时内变化情况
var order_count_hourly = function (data_count, width) {
	var _width = width, _height = 400,
		_margins = {top: 50, left: 80, right: 50, bottom: 30};

	var dataset = data_count;

	var y_max = d3.max(dataset, function (d) {
		return d[1];
	});

	var svg = d3.select('.orders-hourly')
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
		return '24小时成功下单变化图';
	};

	svg.append('text')
		.text(_get_title())
		.attr('class', 'title')
		.attr('x', _width/4)
		.attr('y', 25)
		.attr('font-size', '18px');

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
			return dataset[d][0]+'点';
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
		.text('订单数（个）')
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
			return x_scale(i) + _margins.left;
		})
		.attr('y', function (d) {
			return y_scale(d[1]) + _margins.top + 15;
		})
		.attr('font-size', '12px')
		.attr('fill', '#F36');
};

// 每月销售额的变化趋势
var order_amount_monthly = function (data_amount, width) {
	var _width = width, _height = 400,
		_margins = {top: 50, left: 80, right: 50, bottom: 30};

	var dataset = data_amount;

	var y_max = d3.max(dataset, function (d) {
		return d[1];
	});

	var svg = d3.select('.amount-monthly')
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
		return dataset[0][0] + '至' + dataset[dataset.length - 1][0] + '销售额趋势图';
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
			return number_format(d[1]);
		})
		.attr('x', function (d, i) {
			var x = x_scale(i) + _margins.left + 15;
			if (x > _width - _margins.left - _margins.right) {
				x = _width - _margins.left - _margins.right;
			}
			return x;
		})
		.attr('y', function (d) {
			return y_scale(d[1]) + _margins.top + 15;
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
		.text('销售额（元）')
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

// 每月订单数变化趋势
var order_count_monthly = function (data_count, width) {
	var _width = width, _height = 400,
		_margins = {top: 50, left: 80, right: 50, bottom: 30};

	var dataset = data_count;

	var y_max = d3.max(dataset, function (d) {
		return d[1];
	});

	var svg = d3.select('.orders-monthly')
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
		return dataset[0][0] + '至' + dataset[dataset.length - 1][0] + '订单数趋势图';
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
			return x_scale(i) + _margins.left + 15;
		})
		.attr('y', function (d) {
			return y_scale(d[1]) + _margins.top + 15;
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
		.text('订单数（个）')
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

// 渠道分布饼图
var order_channel_stats = function (dataset, width) {
	var _width = width, _height = 400,
		_margins = {top: 30, left: 50, right: 150, bottom: 30};

	var dataset = dataset;

	// 转化数据为适合生成饼图的对象数组
	var pie = d3.layout.pie()
				.value(function (d) {
					return d[1];
				});
	var piedata = pie(dataset);

	var outerRadius = _width/6; // 外半径
	var innerRadius = _width/8.5; // 内半径

	var svg = d3.select('.sale-channels')
				.append('svg')
				.style('text-align', 'center')
				.attr('class', 'd3chart')
				.attr('width', _width - _margins.left - _margins.right)
				.attr('height', _height + _margins.top + _margins.bottom);
	// 颜色函数
	var _colors = d3.scale.category10();

	// 创建弧生成器
	var arc = d3.svg.arc()
		.innerRadius(innerRadius)
		.outerRadius(outerRadius);

	// 准备分组，把每个分组移到图表中心
	var arcs = svg.selectAll('g.arc')
		.data(piedata)
		.enter()
		.append('g')
		.attr('class', 'arc')
		.attr('transform', 'translate('+ outerRadius +', '+ outerRadius +')');

	// 添加弧的路径元素
	arcs.append('path')
		.attr('fill', function (d, i) {
			return _colors(i);
		})
		.attr('d', arc);

	// 添加弧内的文字
	arcs.append('text')
		.attr('transform', function (d) {
			return 'translate('+ arc.centroid(d) +')';
		})
		.attr('text-anchor', 'middle')
		.text(function (d) {
			// 计算百分比
			var percent = Number(d.value)/d3.sum(dataset, function (d) {
					return d[1];
				})*100;
			// 保留一位小数点，末尾加一个百分号
			return percent.toFixed(1)+'%';
		});

	// 添加图例
	var legend = svg.selectAll('.legend')
		.data(_colors.domain())
		.enter()
		.append('g')
		.attr('class', 'legend')
		.attr('transform', function (d, i) {
			var l_x = i * 140 ;
			var l_y = _height + _margins.top;
			return 'translate('+ l_x +', '+ l_y +')';
		});

	legend.append('rect')
		.attr('x', 0)
		.attr('y', 1)
		.attr('width', 16)
		.attr('height', 8)
		.style('fill', _colors);

	legend.append('text')
		.attr('x', 25)
		.attr('y', 9)
		.classed('legendtext', true)
		.text(function (d) {
			return dataset[d][0] + ' / ' + dataset[d][1] +'个';
		});
};

// 客单价范围
var order_money_stats = function (dataset, width) {
	var _width = width, _height = 400, _rect_padding = 20;
		_margins = {top: 50, left: 80, right: 50, bottom: 30};

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
				x_label += '大于等于';
			} else if (dataset[d][0] >= 3000) {
				x_label += '小于等于';
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
		.text('订单数（个）')
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


// 复购率
var order_repurchase_stats = function (data_count, width) {
		var _width = width, _height = 400, _rect_padding = 20;
		_margins = {top: 50, left: 80, right: 50, bottom: 30};

	var dataset = data_count;

	var y_max = d3.max(dataset, function (d) {
		return d[1];
	});

	var svg = d3.select('.repurchase-stats')
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
			if (dataset[d][0] >= 10) {
				x_label += '大于等于';
			} else {
				x_label += '';
			}
			x_label +=  dataset[d][0] + '次';
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
		.text('订单数（个）')
		.attr('x', 10)
		.attr('y', -30)
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

// 地区分布
var order_area_stats = function (dataset, width) {
	var _width = width, _height = 600;

	var dataset = dataset;

	var data_s = [],
		data_m = [],
		data_idx = [];

	for (var i=0; i<dataset.length; i++) {
		var name = dataset[i][0];
		var value = dataset[i][1];
		if (name == '内蒙') {
			name += '古';
		} else if (name == '黑龙') {
			name += '江';
		}
		data_s[name] = value;
		data_m.push(value);
		data_idx[name] = i+1;
	}

	var max_data = d3.max(dataset, function (d) {
		return d[1];
	});

	var min_data = 0;

	var linear = d3.scale.linear()
		.domain([min_data, max_data])
		.range([0, 1]);
	// 定义颜色
	var b = d3.rgb(255, 51, 102);
	var a = d3.rgb(255, 204, 204);
	// 设置颜色插值
	var color = d3.interpolate(a, b);

	var svg = d3.select('.sale-area')
		.append('svg')
		.attr('width', _width)
		.attr('height', _height)
		.append('g')
		.attr('transform', 'translate(0, 0)');

	var projection = d3.geo.mercator()
		.center([107, 31])
		.scale(550)
		.translate([_width/2, _height/2]);

	var path = d3.geo.path()
		.projection(projection);

	d3.json('http://frstatic.qiniudn.com/china.geojson', function (error, root) {
		if (error) {
			return console.error(error);
		}

		var tooltip = d3.select('body')
			.append('div')
			.attr('opacity', 0.0)
			.attr('class', 'tooltip');

		var provinces = svg.selectAll('path')
				.data( root.features )
				.enter()
				.append('path')
				.attr('stroke', '#000')
				.attr('stroke-width', 1)
				.attr('fill', function (d, i) {
					return '#ccc';
				})
				.attr('d', path);

		provinces.style('fill', function (d, i) {
				var t = linear(data_s[d.properties.name]);
				var col = color(t);
				return col.toString();
			})
			.on('mouseover', function (d, i) {
				d3.select(this)
					.attr('fill', '#ccc');

				tooltip.html(d.properties.name + ' : ' + data_s[d.properties.name] + '个，排名：' + data_idx[d.properties.name])
					.style('left', (d3.event.pageX) + 'px')
					.style('top', (d3.event.pageY) + 'px')
					.style('opacity', 1.0);
			})
			.on('mouseout', function (d, i) {
				d3.select(this)
					.attr('fill', color(i));

				tooltip.style('opacity', 0.0);
			});

		// 显示渐变矩形条
		var defs = svg.append('defs');

		var linearGradient = defs.append('linearGradient')
			.attr('id', 'linearColor')
			.attr('x1', '0%')
			.attr('y1', '0%')
			.attr('x2', '100%')
			.attr('y2', '0%');

		var stop1 = linearGradient.append('stop')
			.attr('offset', '0%')
			.attr('stop-color', a.toString());
		var stop2 = linearGradient.append('stop')
			.attr('offset', '100%')
			.attr('stop-color', b.toString());
		var color_rect = svg.append('rect')
			.attr('x', 40)
			.attr('y', 35)
			.attr('width', 200)
			.attr('height', 20)
			.style('fill', 'url(#'+ linearGradient.attr('id') +')');
		var start_text = svg.append('text')
			.attr('x', 40)
			.attr('y', 30)
			.text(min_data);
		var mid_text = svg.append('text')
			.attr('x', 125)
			.attr('y', 30)
			.text(d3.median(data_m));
		var end_text = svg.append('text')
			.attr('x', 240)
			.attr('y', 30)
			.text(max_data);


		var l_title = svg.append('text')
			.attr('x', 30)
			.attr('y', _height - _margins.bottom - _margins.top - 30)
			.text('TOP10的省市');

		// 添加图例
		for (var i=0; i<10; i++) {
			// 计算百分比
			var percent = Number(dataset[i][1])/d3.sum(dataset, function (d) {
					return d[1];
				})*100;
			var _text = (i+1) +'、'+ dataset[i][0] + ' ' + percent.toFixed(1)+'%';
			var _y = _height - _margins.bottom - _margins.top;
			var _x = i;
			if (i >= 5) {
				_x -= 5;
				_y += 20;
			}
			svg.append('text')
				.attr('x', _x*120 + 25)
				.attr('y', _y)
				.attr('width', 120)
				.attr('height', 20)
				.text(_text);
		}

	});




};