import os
import sys
import re

import inspect
import seaborn as sns
import pandas as pd
import numpy as np
import itertools
from statannot import add_stat_annotation

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import transforms
from matplotlib.artist import Artist

import matplotlib.patheffects as PathEffects

from .util import *

def savefig_with_readme(args, stack, path_fig):

	plt.savefig(path_fig)
	
	dirname = os.path.dirname(path_fig)
	path_readme = os.path.join(dirname, 'README.txt')
	
	path_script = stack[0][1]
	
	text_stack = ['line: ' + str(trace[2]) + ', ' + str(trace[4][0]) for i, trace in enumerate(stack) if i > 0]
	text_stack.reverse()
	
	text_readme = '\n'.join(['Figures generated with: ' + path_script, 'Input arguments: ' + str(args), 'Stack:\n']) + ''.join(text_stack)
	
	with open(path_readme, 'w') as file:
		file.write(text_readme)

def newline(p1, p2):
	ax = plt.gca()
	xmin, xmax = ax.get_xbound()

	if(p2[0] == p1[0]):
		xmin = xmax = p1[0]
		ymin, ymax = ax.get_ybound()
	else:
		ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
		ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])

	l = mlines.Line2D([xmin,xmax], [ymin,ymax])
	ax.add_line(l)
	return l

def newtext(s, corner, **kwargs):
	ax = plt.gca()
	xmin, xmax = ax.get_xbound()
	ymin, ymax = ax.get_ybound()

	if corner == 'top-right':
		x = xmax * 0.98
		y = ymax * 0.98
		plt.text(x,y,s, horizontalalignment='right', verticalalignment = 'top', **kwargs)
	elif corner == 'top-left':
		x = xmin + (xmax - xmin)*0.02
		y = ymax * 0.98
		plt.text(x,y,s, horizontalalignment='left', verticalalignment = 'top', **kwargs)
	elif corner == 'bottom-left':
		x = xmin + (xmax - xmin)*0.02
		y = ymin + (ymax - ymin)*0.02
		plt.text(x,y,s, horizontalalignment='left', verticalalignment = 'bottom', **kwargs)
	elif corner == 'bottom-right':
		x = xmax * 0.98
		y = ymin + (ymax - ymin)*0.02
		plt.text(x,y,s, horizontalalignment='right', verticalalignment = 'bottom', **kwargs)

def add_metric_to_box_plot(df, x, y, order, ax, metric, **kwargs):
	
	unique_xs = order
	metrics = {}
	medians = {}
	pos = {}
	
	for i, unique_x in enumerate(unique_xs):
		df_x = df.loc[df[x] == unique_x]
		
		if metric == 'mean':
			metric_y = np.mean(df_x[y].tolist())
		elif metric == 'median':
			metric_y = np.median(df_x[y].tolist())
			
		median_y = np.median(df_x[y].tolist())
		
		metrics[unique_x] = metric + "=" + str(round(metric_y,3))
		medians[unique_x] = median_y
		pos[unique_x] = i
		
	# horizontalalignment='center', fontsize='x-small', color='w'
	 
	# Add it to the plot
	for tick, label in zip(pos, ax.get_xticklabels()):
		txt = ax.text(pos[tick], medians[tick] + 0.03, metrics[tick], **kwargs)
		txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])
		
def add_n_to_box_plot(df, x, y, order, ax, **kwargs):
	
	unique_xs = order
	medians = {}
	nobs = {}
	pos = {}
	
	for i, unique_x in enumerate(unique_xs):
		df_x = df.loc[df[x] == unique_x]
		nob = str(len(df_x.index))
		median_y = np.median(df_x[y].tolist())
		
		medians[unique_x] = median_y
		nobs[unique_x] = "n=" + nob
		pos[unique_x] = i
		
	# horizontalalignment='center', fontsize='x-small', color='w'
	 
	# Add it to the plot
	for tick, label in zip(pos, ax.get_xticklabels()):
		ax.text(pos[tick], medians[tick] + 0.03, nobs[tick], **kwargs)
		
def set_size(w,h, ax=None):
	""" w, h: width, height in inches """
	if not ax: ax=plt.gca()
	l = ax.figure.subplotpars.left
	r = ax.figure.subplotpars.right
	t = ax.figure.subplotpars.top
	b = ax.figure.subplotpars.bottom
	figw = float(w)/(r-l)
	figh = float(h)/(t-b)
	ax.figure.set_size_inches(figw, figh)

def plot_kde(df, x_name, filename, path_plot_dir, font_sizes=None, xlim=None, title=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	
	sns.kdeplot(data=df, x=x_name, ax=ax, **kwargs)
		
	if xlim is not None:
		ax.set_xlim(xlim)
	
	# plot for viewing
	path_png = os.path.join(path_plot_dir, filename + '.png')
	plt.title(title)
	plt.show()
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()	

def plot_scatter(df, x, y, filename, path_plot_dir, font_sizes=None, ylim=None, xlim=None, xlabel=None, ylabel=None, title=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	
	ax = sns.scatterplot(data=df, x=x, y=y, **kwargs)
	
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	
	if ylim is not None:
		ax.set_ylim(ylim)
		
	if xlim is not None:
		ax.set_xlim(xlim)	
	
	if title is not None:
		plt.title(title)
		
	plt.tight_layout()
	
	path_png = os.path.join(path_plot_dir, filename + '.png')
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	
	path_svg = os.path.join(path_plot_dir, filename + '.svg')
	savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
	
	plt.close()

def plot_2d_kde(x, y, filename, path_plot_dir, font_sizes=None, ylim=None, xlim=None, xlabel=None, ylabel=None, title=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	
	ax = sns.kdeplot(x=x, y=y, **kwargs)
	
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	
	if ylim is not None:
		ax.set_ylim(ylim)
		
	if xlim is not None:
		ax.set_xlim(xlim)	
	
	if title is not None:
		plt.title(title)
		
	plt.tight_layout()
		
	path_png = os.path.join(path_plot_dir, filename + '.png')
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	
	path_svg = os.path.join(path_plot_dir, filename + '.svg')
	savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
	
	plt.close()


def plot_scatter_list(x, y, filename, path_plot_dir, font_sizes=None, ylim=None, xlim=None, xlabel=None, ylabel=None, title=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	
	ax = sns.scatterplot(x=x, y=y, **kwargs)
	
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	
	if ylim is not None:
		ax.set_ylim(ylim)
		
	if xlim is not None:
		ax.set_xlim(xlim)	
	
	if title is not None:
		plt.title(title)
		
	plt.show()
	path_png = os.path.join(path_plot_dir, filename + '.png')
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()
	
def plot_hist(df, x_name, filename, path_plot_dir, font_sizes=None, ylim=None, xlim=None, title=None, xlabel=None, ylabel=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	
	sns.histplot(data=df, x=x_name, ax=ax, **kwargs)
	
	if ylim is not None:
		ax.set_ylim(ylim)
		
	if xlim is not None:
		ax.set_xlim(xlim)
		
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	
	# plot for viewing
	path_png = os.path.join(path_plot_dir, filename + '.png')
	plt.title(title)
	plt.show()
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()	

def plot_hist_list(data_list, filename, path_plot_dir, font_sizes=None, ylim=None, xlim=None, title=None, xlabel=None, ylabel=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	
	sns.histplot(data_list, ax=ax, **kwargs)
	
	if ylim is not None:
		ax.set_ylim(ylim)
		
	if xlim is not None:
		ax.set_xlim(xlim)
		
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	
	# plot for viewing
	path_png = os.path.join(path_plot_dir, filename + '.png')
	plt.title(title)
	plt.show()
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()
	
def plot_violin(df, x, y, order, filename, path_plot_dir, font_sizes=None, fig_width=None, fig_height=None, palette_name=None, metric=None, stat_test=None, rotate_x=False, xlabel=None, ylabel=None, ylim=None, hue=None, hue_order=None, pad_top=False, pad_bottom=False, pad_left=False, pad_right=False, title=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	if pad_top and pad_bottom:
		fig, ax = plt.subplots(figsize = (8, 10))
	elif (pad_top and not pad_bottom) or (pad_bottom and not pad_top):
		fig, ax = plt.subplots(figsize = (8, 8))
	else:
		fig, ax = plt.subplots()
		
	if pad_top:
		fig.subplots_adjust(top=0.55)
	if pad_bottom:
		fig.subplots_adjust(bottom=0.45)
	if pad_left:
		fig.subplots_adjust(left=0.25)
	if pad_right:
		fig.subplots_adjust(right=0.85)
	
	#palette=sns.color_palette(palette_name, n_colors=len(order))
		
	# in a violin plot, 'x' serves as the hue
		
	if hue is not None and hue_order is not None:
		# for when there are inner categories
		sns.violinplot(data=df, x=x, y=y, ax=ax, order=order, hue=hue, hue_order=hue_order, **kwargs)
		if stat_test is not None:
			inner_categories = list(set(df[hue].tolist()))
			x_pairs = [((outer_category, inner_pair[0]), (outer_category, inner_pair[1])) for inner_pair in list(itertools.combinations(inner_categories, 2)) for outer_category in order]
			add_stat_annotation(ax, data=df, x=x, y=y, order=order, box_pairs=x_pairs, hue=hue, test=stat_test, text_format='star', fontsize=SMALL_SIZE, loc='inside', verbose=0, linewidth=1, color='black')
	else:
		# only one set of categories
		sns.violinplot(data=df, x=x, y=y, ax=ax, order=order, **kwargs)
		if stat_test is not None:
			x_pairs = list(itertools.combinations(order, 2))
			add_stat_annotation(ax, data=df, x=x, y=y, order=order, box_pairs=x_pairs, test=stat_test, text_format='star', fontsize=SMALL_SIZE, loc='inside', verbose=0, linewidth=1, color='black')
	
	if ylim is not None:
		ax.set_ylim(ylim)
	
	if metric is not None:
		add_metric_to_box_plot(df, x, y, order, ax, metric)
	
	path_png = os.path.join(path_plot_dir, filename + '.png')
	path_svg = path_png.replace('.png', '.svg')
	
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	
	if rotate_x:
		plt.xticks(rotation=45, ha='right')
	
	if title is not None:
		plt.title(title)
		
	plt.tight_layout()
		
	plt.show()
	
	if fig_width is not None and fig_height is not None:
		set_size(fig_width, fig_height, ax)
	
	savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()	
	
def plot_box(df, x, y, order, filename, path_plot_dir, font_sizes=None, fig_width=None, fig_height=None, palette_name=None, metric=None, add_n=False, add_stat=False, rotate_x=False, xlabel=None, ylabel=None, ylim=None, hue=None, hue_order=None, pad_top=False, pad_bottom=False, pad_left=False, pad_right=False, title=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	if pad_top:
		fig.subplots_adjust(top=0.55)
	if pad_bottom:
		fig.subplots_adjust(bottom=0.25)
	if pad_left:
		fig.subplots_adjust(left=0.25)
	if pad_right:
		fig.subplots_adjust(right=0.85)
	
	#palette=sns.color_palette(palette_name, n_colors=len(order))
		
	if hue is not None and hue_order is not None:
		sns.boxplot(data=df, x=x, y=y, ax=ax, order=order, hue=hue, hue_order=hue_order, **kwargs)
		if add_stat:
			inner_categories = list(set(df[hue].tolist()))
			x_pairs = [((outer_category, inner_pair[0]), (outer_category, inner_pair[1])) for inner_pair in list(itertools.combinations(inner_categories, 2)) for outer_category in order]
			add_stat_annotation(ax, data=df, x=x, y=y, order=order, box_pairs=x_pairs, hue=hue, test='t-test_ind', text_format='star', fontsize=SMALL_SIZE, loc='outside', verbose=0, linewidth=1, color='black')
	else:
		sns.boxplot(data=df, x=x, y=y, ax=ax, order=order, **kwargs)
		if add_stat:
			x_pairs = list(itertools.combinations(order, 2))
			add_stat_annotation(ax, data=df, x=x, y=y, order=order, box_pairs=x_pairs, test='t-test_ind', text_format='full', fontsize=SMALL_SIZE, loc='outside', verbose=0, linewidth=1, color='black')
		
	if ylim is not None:
		ax.set_ylim(ylim)
	
	if add_n:
		add_n_to_box_plot(df, x, y, order, ax)
	
	path_png = os.path.join(path_plot_dir, filename + '.png')
	path_svg = path_png.replace('.png', '.svg')
	
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	
	if metric is not None:
		add_metric_to_box_plot(df, x, y, order, ax, metric, ha='center')
	
	if rotate_x:
		plt.xticks(rotation=45, ha='right')
	
	if title is not None:
		plt.title(title)
	
	if fig_width is not None and fig_height is not None:
		set_size(fig_width, fig_height, ax)
		
	plt.tight_layout()
	plt.show()
	
	savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()
	
def scale_num(new_max, new_min, old_max, old_min, val):
	return (new_max - new_min) * (val - old_min) / (old_max - old_min) + new_min
	
def rainbow_text(x, y, strings, colors, weights, ha, spacing, **kw):
	"""
	Take a list of strings ``strings`` and colors ``colors`` and place them next to each
	other, with text strings[i] being shown in color colors[i].
	
	x and y are axes coordinates, not data coordinates
	"""
	t = plt.gca().transAxes
	fig = plt.gcf()
	plt.show()
	
	#horizontal version
	newline_offset = 0
	first_t = False
	line_widths = []
	line_width = 0
	text_objects = []
	
	if ha == 'left':
		for s,c,w in zip(strings, colors, weights):
				
			if s != '\n':
				text = plt.text(x, y, s+" ", color=c, transform=t, fontweight=w, **kw)
				text.draw(fig.canvas.get_renderer())
				
				ex = text.get_window_extent()
				t = transforms.offset_copy(text._transform, x=ex.width, units='dots')
				
				if not first_t:
					first_t = text._transform
				
			else:
				# reset the x transform, add onto y transform
				# 1.5 spacing
				newline_offset += (ex.height * spacing)
				t = transforms.offset_copy(first_t, y=-newline_offset, units='dots')
				
	elif ha == 'center':
	
		# draw entire line first to get line widths
		for s,c,w in zip(strings, colors, weights):
				
			if s != '\n':
				text = plt.text(x, y, s+" ", color=c, transform=t, fontweight=w, **kw)
				text.draw(fig.canvas.get_renderer())
				text_objects.append(text)
				
				ex = text.get_window_extent()
				t = transforms.offset_copy(text._transform, x=ex.width, units='dots')
				line_width += ex.width
				
				if not first_t:
					first_t = text._transform
				
			else:
				# reset the x transform, add onto y transform
				# 1.5 spacing
				newline_offset += (ex.height * spacing)
				t = transforms.offset_copy(first_t, y=-newline_offset, units='dots')
				line_widths.append(line_width)
				line_width = 0
				
		line_widths.append(line_width)
		line_h_offsets = [-width/2 for width in line_widths]
		
		t = plt.gca().transAxes
		newline_offset = 0
		
		# delete now that we have offset
		for text_object in text_objects:
			Artist.remove(text_object)
			
		i_line = 0
		t = transforms.offset_copy(first_t, x=line_h_offsets[i_line], units='dots')
		i_line += 1
			
		# redraw
		for s,c,w in zip(strings, colors, weights):
			
			if s != '\n':
				text = plt.text(x, y, s+" ", color=c, transform=t, fontweight=w, **kw)
				text.draw(fig.canvas.get_renderer())
				
				ex = text.get_window_extent()
				t = transforms.offset_copy(text._transform, x=ex.width, units='dots')
				line_width += ex.width
				
			else:
				# reset the x transform, add onto y transform
				# 1.5 spacing
				newline_offset += (ex.height * spacing)
				t = transforms.offset_copy(first_t, y=-newline_offset, x=line_h_offsets[i_line], units='dots')
				i_line += 1
	
def plot_line(df, x_name, y_name, filename, path_plot_dir, font_sizes=None, hue=None, custom_ci_names=None, xlim=None, ylim=None, title=None, fig_width=None, fig_height=None, xticks=None, xlabels=None, xlabel=None, yticks=None, ylabels=None, ylabel=None, legend_text=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	
	if hue is not None:
		
		hue_order = list(set(df[hue].tolist()))
		hue_order.sort(key=natural_keys)
		palette=sns.color_palette("mako", n_colors=len(hue_order))
		palette.reverse()
		
		# ci = 1.96 * np.std(y)/np.sqrt(len(x))
	
		if custom_ci_names is not None:
			lower_bound_name = custom_ci_names[0]
			upper_bound_name = custom_ci_names[1]
			for i, group in enumerate(hue_order):
				df_hue = df.loc[df[hue] == group]
				x = df_hue[x_name].tolist()
				lower_bound = df_hue[lower_bound_name].tolist()
				upper_bound = df_hue[upper_bound_name].tolist()
				plt.fill_between(x, lower_bound, upper_bound, color=palette[i], alpha=.33)
				
		
		# make a custom legend. we have the colors
		if legend_text is not None:
			sns.lineplot(data=df, x=x_name, y=y_name, hue=hue, hue_order=hue_order, ax=ax, palette=palette, legend=False, **kwargs)
			num_words = len(legend_text.split(' '))
			legend_lines = ' '.join(['|' for i in hue_order])
			legend_descriptor = r'Low $\rightarrow$ High'
			
			legend_text = f'{legend_text} \n {legend_lines} \n {legend_descriptor}'.split(' ')
			
			legend_colors = [(0.0, 0.0, 0.0)] * (num_words + 1) + palette + [(0.0, 0.0, 0.0)] * 4
			legend_weights = ['normal'] * (num_words + 1) + ['bold'] * len(palette) + ['normal'] * 4
			
			ha = 'center'
			spacing = 1.5
			
			rainbow_text(1.2, 0.5, legend_text, legend_colors, legend_weights, ha, spacing)
			
		else:
			sns.lineplot(data=df, x=x_name, y=y_name, hue=hue, hue_order=hue_order, ax=ax, palette=palette, **kwargs)
			plt.legend()
		
	else:
		sns.lineplot(data=df, x=x_name, y=y_name, ax=ax, **kwargs)
	
	if ylim is not None:
		ax.set_ylim(ylim)
	
	if xlim is not None:
		ax.set_xlim(xlim)
		
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	
	if xticks is not None:
		ax.set_xticks(xticks)
		if xlabels is not None:
			ax.set_xticklabels(xlabels)	
		
	if yticks is not None:
		ax.set_yticks(yticks)
		if ylabels is not None:
			ax.set_yticklabels(ylabels)
			
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
		
	# plot for viewing
	path_png = os.path.join(path_plot_dir, filename + '.png')
	path_svg = path_png.replace('.png', '.svg')
	
	plt.title(title)
	
	# add some padding on right side for custom legend
	if legend_text is not None:
		plt.tight_layout(rect = (0, 0, 1, 1))
	
	plt.show()
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
	
	# plot for final figure
	if fig_width is not None and fig_height is not None:
		set_size(fig_width, fig_height, ax)
		
		path_png = os.path.join(path_plot_dir, filename + '.for_figure.png')
		path_svg = path_png.replace('.png', '.svg')
		
		savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
		savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
		
	plt.close()
	
def plot_bar(df, x, y, order, filename, path_plot_dir, font_sizes = None, fig_width=None, fig_height=None, add_n=False, add_stat=False, rotate_x=False, xlabel=None, ylabel=None, ylim=None, hue=None, hue_order=None, **kwargs):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	fig.subplots_adjust(left=0.25, right=0.85, top=0.55, bottom=0.25)
	
	if hue is not None and hue_order is not None:
		sns.barplot(data=df, x=x, y=y, ax=ax, hue=hue, order=order, hue_order=hue_order, **kwargs)
		if add_stat:
			inner_categories = list(set(df[hue].tolist()))
			x_pairs = [((outer_category, inner_pair[0]), (outer_category, inner_pair[1])) for inner_pair in list(itertools.combinations(inner_categories, 2)) for outer_category in order]
			add_stat_annotation(ax, data=df, x=x, y=y, order=order, box_pairs=x_pairs, hue=hue, test='t-test_ind', text_format='star', fontsize=SMALL_SIZE, loc='outside', verbose=0, linewidth=1, color='black')
	else:
		sns.barplot(data=df, x=x, y=y, ax=ax, order=order, hue=hue, **kwargs)
		if add_stat:
			x_pairs = list(itertools.combinations(order, 2))
			add_stat_annotation(ax, data=df, x=x, y=y, order=order, box_pairs=x_pairs, test='t-test_ind', text_format='star', fontsize=SMALL_SIZE, loc='outside', verbose=0, linewidth=1, color='black')
	
	path_png = os.path.join(path_plot_dir, filename + '.png')
	path_svg = path_png.replace('.png', '.svg')
	
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
		
	if ylim is not None:
		ax.set_ylim(ylim)
		
	if add_n:
		add_n_to_bar_plot(df, x, y, order, ax)
	
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	
	if rotate_x:
		plt.xticks(rotation=45, ha='right')
	
	plt.title(filename)
	plt.show()
	
	if fig_width is not None and fig_height is not None:
		set_size(fig_width, fig_height, ax)
	
	savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()
	
def add_n_to_bar_plot(df, x, y, order, ax):
	
	unique_xs = order
	means = {}
	nobs = {}
	pos = {}
	
	for i, unique_x in enumerate(unique_xs):
		df_x = df.loc[df[x] == unique_x]
		nob = str(len(df_x.index))
		mean_y = np.mean(df_x[y].tolist())
		
		means[unique_x] = mean_y
		nobs[unique_x] = "n=" + nob
		pos[unique_x] = i
	 
	# Add it to the plot
	for tick, label in zip(pos, ax.get_xticklabels()):
		ax.text(pos[tick], means[tick] + 0.1, nobs[tick], horizontalalignment='left', color='black', fontsize=SMALL_SIZE, rotation=45)

def add_stdev(df, x, y, order, ax, colors=None):
	
	lines = {}
	means = {}
	pos = {}
	colors_dict = {}
	
	for i, unique_x in enumerate(order):
	
		df_x = df.loc[df[x] == unique_x]
		
		mean_y = np.mean(df_x[y].tolist())
		#standard_err = stats.sem(df_x[y].tolist())
		standard_err = np.std(df_x[y].tolist())
		
		means[unique_x] = mean_y
		lines[unique_x] = [[i, mean_y-standard_err],[i, mean_y+standard_err]]
		pos[unique_x] = i
		colors_dict[unique_x] = colors[i]
	 
	# Add it to the plot
	for tick, label in zip(pos, ax.get_xticklabels()):
		if colors is not None:
			newline(lines[tick][0], lines[tick][1], color=colors_dict[tick])
			plt.plot(pos[tick], means[tick], marker='D', markersize=3, color=colors_dict[tick])
		else:
			newline(lines[tick][0], lines[tick][1])
			plt.plot(pos[tick], means[tick], marker='D', markersize=3)


def plot_mean_and_sem(df, x, y, order, filename, path_plot_dir, font_sizes=None, fig_width=None, fig_height=None, colors=None, rotate_x=False, xlabel=None, ylabel=None, ylim=None):
	
	if font_sizes is not None:
		if font_sizes == 'powerpoint':
			set_powerpoint_sizes()
		elif font_sizes == 'article':
			set_article_sizes()
	
	fig, ax = plt.subplots()
	fig.subplots_adjust(left=0.25, right=0.85, top=0.55, bottom=0.25)
	
	plt.xticks(ticks=list(range(len(order))), labels=order)
	
	add_stdev(df, x, y, order, ax, colors=colors)
	
	path_png = os.path.join(path_plot_dir, filename + '.png')
	path_svg = path_png.replace('.png', '.svg')
	
	if xlabel is not None:
		ax.set_xlabel(xlabel)
		
	if ylabel is not None:
		ax.set_ylabel(ylabel)
		
	if ylim is not None:
		ax.set_ylim(ylim)
		
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	
	if rotate_x:
		plt.xticks(rotation=45, ha='right')
	
	plt.title(filename)
	plt.show()
	
	if fig_width is not None and fig_height is not None:
		set_size(fig_width, fig_height, ax)
	
	savefig_with_readme(str(sys.argv), inspect.stack(), path_svg)
	savefig_with_readme(str(sys.argv), inspect.stack(), path_png)
	plt.close()
