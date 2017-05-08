# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from flask import g, current_app, request, redirect, url_for, render_template,flash
from app.main import main
from app.models import Rule
from app.forms import RuleForm

@main.route('/rules')
def rule_list():
    rules = Rule.objects.all()
    return render_template('rules/index.html',
                           rules=rules)


@main.route('/rules/<string:id>')
def rule_show(id):
    pass


@main.route('/rules/create', methods=['GET', 'POST'])
def rule_create():
    rule = {}

    form = RuleForm()
    if form.validate_on_submit():
        rule = Rule()

        rule.site = form.data.get('site')
        rule.name = form.data.get('name')
        rule.allow_domains = form.data.get('allow_domains')
        rule.start_urls = form.data.get('start_urls')
        rule.next_page = form.data.get('next_page')
        rule.allow_url = form.data.get('allow_url')
        rule.extract_from = form.data.get('extract_from')
        rule.title_xpath = form.data.get('title_xpath')
        rule.meta_xpath = form.data.get('meta_xpath')
        rule.image_xpath = form.data.get('image_xpath')
        rule.price_xpath = form.data.get('price_xpath')
        rule.original_price_xpath = form.data.get('original_price_xpath')
        rule.shop_name_xpath = form.data.get('shop_name_xpath')
        rule.enabled = form.data.get('enabled')
        rule.save()

        flash('add new rule is ok!')

        return redirect(url_for('main.rule_list'))

    return render_template('rules/create.html',
                           form=form,
                           rule=rule,
                           )


@main.route('/rules/<string:id>/update', methods=['GET', 'POST'])
def rule_update(id):
    rule = Rule.objects.get_or_404(_id=ObjectId(id))

    form = RuleForm()

    if form.validate_on_submit():

        # update data of changes
        some_data = {}

        some_data['site'] = form.data.get('site')
        some_data['name'] = form.data.get('name')
        some_data['allow_domains'] = form.data.get('allow_domains')
        some_data['start_urls'] = form.data.get('start_urls')
        some_data['next_page'] = form.data.get('next_page')
        some_data['allow_url'] = form.data.get('allow_url')
        some_data['extract_from'] = form.data.get('extract_from')
        some_data['title_xpath'] = form.data.get('title_xpath')
        some_data['meta_xpath'] = form.data.get('meta_xpath')
        some_data['image_xpath'] = form.data.get('image_xpath')
        some_data['price_xpath'] = form.data.get('price_xpath')
        some_data['original_price_xpath'] = form.data.get('original_price_xpath')
        some_data['shop_name_xpath'] = form.data.get('shop_name_xpath')
        some_data['enabled'] = form.data.get('enabled')

        # do it.
        rule.update(**some_data)

        flash('update the rule is ok!')

        return redirect(url_for('main.rule_list'))

    return render_template('rules/edit.html',
                           form=form,
                           rule=rule)


@main.route('/rules/<string:id>/destroy', methods=['GET'])
def rule_destroy(id):
    rule = Rule.objects.get_or_404(_id=ObjectId(id))
    rule.delete()

    flash('delete the rule is ok!')

    return  redirect(url_for('main.rule_list'))
