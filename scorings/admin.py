from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import Scoring, LevelCurrent


class AddScoreForm(forms.Form):
    """Form to add score to selected users"""
    score_to_add = forms.IntegerField(
        label='Score hinzufügen',
        min_value=-2000,
        max_value=2000,
        help_text='Anzahl der Punkte, die hinzugefügt werden sollen'
    )


class SetScoreForm(forms.Form):
    """Form to set score for selected users"""
    score_to_set = forms.IntegerField(
        label='Score setzen',
        min_value=0,
        max_value=2000,
        help_text='Exakte Punktzahl (0 = schlecht, 1000 = ausgeglichen, 2000 = maximum)'
    )


class AddXPForm(forms.Form):
    """Form to add XP to selected users"""
    xp_to_add = forms.IntegerField(
        label='XP hinzufügen',
        min_value=1,
        help_text='Anzahl der XP, die hinzugefügt werden sollen'
    )


class SetXPForm(forms.Form):
    """Form to set XP for selected users"""
    xp_to_set = forms.IntegerField(
        label='XP setzen',
        min_value=0,
        help_text='Gesamt-XP, auf die gesetzt werden soll'
    )


@admin.register(Scoring)
class ScoringAdmin(admin.ModelAdmin):
    list_display = ['user', 'value', 'score_progress_bar', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['score_info_display']
    
    fields = ['user', 'value', 'score_info_display']
    
    actions = ['add_score_to_users', 'set_score_for_users']
    
    def score_progress_bar(self, obj):
        """Display a progress bar for score (0-2000)"""
        if obj.value is None:
            return format_html('<span style="color: #999;">Noch nicht gesetzt</span>')
        
        percentage = int((obj.value / 2000) * 100)
        percentage = max(0, min(percentage, 100))
        
        # Color based on score range
        if obj.value < 500:
            color = '#FF3B30'  # Red - bad
        elif obj.value < 1000:
            color = '#FF9500'  # Orange - below average
        elif obj.value < 1500:
            color = '#FFCC00'  # Yellow - above average
        else:
            color = '#4CD964'  # Green - excellent
        
        return format_html(
            '<div style="width: 100%; background-color: #ddd; border-radius: 5px; height: 20px;">'
            '<div style="width: {}%; background-color: {}; height: 100%; border-radius: 5px; text-align: center; color: white; line-height: 20px; font-size: 12px;">'
            '{} Pkt'
            '</div>'
            '</div>',
            percentage,
            color,
            obj.value
        )
    score_progress_bar.short_description = 'Score Fortschritt'
    
    def score_info_display(self, obj):
        """Detailed score display"""
        if obj.value is None:
            return format_html(
                '<div style="padding: 15px; background-color: #f0f0f0; border-radius: 5px; text-align: center;">'
                '<p style="color: #666; margin: 0;">Score wird nach dem Speichern angezeigt</p>'
                '<p style="color: #999; font-size: 12px; margin-top: 5px;">Standardwert: 1000 Punkte (ausgeglichen)</p>'
                '</div>'
            )
        
        percentage = int((obj.value / 2000) * 100)
        
        if obj.value < 500:
            rating = 'Schlecht'
            color = '#FF3B30'
        elif obj.value < 1000:
            rating = 'Unterdurchschnittlich'
            color = '#FF9500'
        elif obj.value < 1500:
            rating = 'Überdurchschnittlich'
            color = '#FFCC00'
        else:
            rating = 'Exzellent'
            color = '#4CD964'
        
        return format_html(
            '<div style="margin-bottom: 10px;">'
            '<strong>Aktuelle Punkte:</strong> {}<br>'
            '<strong>Maximum:</strong> 2000 Punkte<br>'
            '<strong>Fortschritt:</strong> {}%<br>'
            '<strong>Bewertung:</strong> <span style="color: {}; font-weight: bold;">{}</span><br>'
            '</div>'
            '<div style="width: 100%; background-color: #ddd; border-radius: 5px; height: 30px; margin-top: 10px;">'
            '<div style="width: {}%; background-color: {}; height: 100%; border-radius: 5px; line-height: 30px; text-align: center; color: white; font-weight: bold;">'
            '{} / 2000'
            '</div>'
            '</div>',
            obj.value,
            percentage,
            color,
            rating,
            percentage,
            color,
            obj.value
        )
    score_info_display.short_description = 'Detaillierte Score-Info'
    
    def add_score_to_users(self, request, queryset):
        """Custom admin action to add score to selected users"""
        if 'apply' in request.POST:
            form = AddScoreForm(request.POST)
            if form.is_valid():
                score_to_add = form.cleaned_data['score_to_add']
                users = queryset.values_list('user', flat=True).distinct()
                
                count = 0
                for user_id in users:
                    # Get latest scoring entry
                    latest_scoring = Scoring.objects.filter(user_id=user_id).order_by('-created_at').first()
                    if latest_scoring:
                        # Create new scoring entry with updated score (capped at 0-2000)
                        new_value = max(0, min(latest_scoring.value + score_to_add, 2000))
                        Scoring.objects.create(
                            user_id=user_id,
                            value=new_value
                        )
                        count += 1
                    else:
                        # Create first scoring entry starting at 1000 (balanced) + added score
                        new_value = max(0, min(1000 + score_to_add, 2000))
                        Scoring.objects.create(
                            user_id=user_id,
                            value=new_value
                        )
                        count += 1
                
                self.message_user(
                    request,
                    f'{score_to_add} Punkte wurden {count} User(n) hinzugefügt.',
                    messages.SUCCESS
                )
                return redirect(request.get_full_path())
        else:
            form = AddScoreForm()
        
        return render(
            request,
            'admin/add_score_form.html',
            context={
                'form': form,
                'users': queryset,
                'title': 'Score hinzufügen'
            }
        )
    
    add_score_to_users.short_description = "Score zu ausgewählten Users hinzufügen"
    
    def set_score_for_users(self, request, queryset):
        """Custom admin action to set exact score for selected users"""
        if 'apply' in request.POST:
            form = SetScoreForm(request.POST)
            if form.is_valid():
                score_to_set = form.cleaned_data['score_to_set']
                users = queryset.values_list('user', flat=True).distinct()
                
                count = 0
                for user_id in users:
                    # Create new scoring entry with exact score
                    Scoring.objects.create(
                        user_id=user_id,
                        value=score_to_set
                    )
                    count += 1
                
                self.message_user(
                    request,
                    f'Score wurde auf {score_to_set} Punkte für {count} User(n) gesetzt.',
                    messages.SUCCESS
                )
                return redirect(request.get_full_path())
        else:
            form = SetScoreForm()
        
        return render(
            request,
            'admin/set_score_form.html',
            context={
                'form': form,
                'users': queryset,
                'title': 'Score setzen'
            }
        )
    
    set_score_for_users.short_description = "Score für ausgewählte Users setzen"


@admin.register(LevelCurrent)
class LevelCurrentAdmin(admin.ModelAdmin):
    list_display = ['user', 'calculated_level', 'xp', 'level_progress_bar', 'xp_to_next_level']
    list_filter = ['xp']
    search_fields = ['user__username', 'user__email']
    ordering = ['-xp']
    readonly_fields = ['level_progress_display', 'xp_info_display']
    
    fields = ['user', 'xp', 'level_progress_display', 'xp_info_display']
    
    actions = ['add_xp_to_users', 'set_xp_for_users']
    
    def calculated_level(self, obj):
        """Display calculated level based on XP"""
        level = obj.get_level()
        return format_html('<strong>Level {}</strong>', level)
    calculated_level.short_description = 'Level (berechnet)'
    
    def level_progress_bar(self, obj):
        """Display a progress bar for level progression"""
        xp_current = obj.get_current_level_xp()
        xp_needed = obj.get_xp_needed_for_next_level()
        
        if xp_needed > 0:
            percentage = int((xp_current / xp_needed) * 100)
        else:
            percentage = 0
        
        # Color based on progress
        if percentage < 25:
            color = '#FF3B30'  # Red
        elif percentage < 50:
            color = '#FF9500'  # Orange
        elif percentage < 75:
            color = '#FFCC00'  # Yellow
        else:
            color = '#4CD964'  # Green
        
        return format_html(
            '<div style="width: 100%; background-color: #ddd; border-radius: 5px; height: 20px;">'
            '<div style="width: {}%; background-color: {}; height: 100%; border-radius: 5px; text-align: center; color: white; line-height: 20px; font-size: 12px;">'
            '{}%'
            '</div>'
            '</div>',
            percentage,
            color,
            percentage
        )
    level_progress_bar.short_description = 'Level Fortschritt'
    
    def xp_to_next_level(self, obj):
        """Show XP needed for next level"""
        xp_current = obj.get_current_level_xp()
        xp_needed = obj.get_xp_needed_for_next_level()
        return format_html(
            '<strong>{}</strong> / {} XP',
            xp_current,
            xp_needed
        )
    xp_to_next_level.short_description = 'XP zum nächsten Level'
    
    def level_progress_display(self, obj):
        """Detailed progress display in detail view"""
        level = obj.get_level()
        xp_current = obj.get_current_level_xp()
        xp_needed = obj.get_xp_needed_for_next_level()
        xp_for_current = obj.xp_for_level(level)
        xp_for_next = obj.xp_for_level(level + 1)
        
        percentage = int((xp_current / xp_needed) * 100) if xp_needed > 0 else 0
        
        return format_html(
            '<div style="margin-bottom: 10px;">'
            '<strong>Berechnetes Level:</strong> {}<br>'
            '<strong>Gesamt XP:</strong> {}<br>'
            '<strong>XP für Level {}:</strong> {}<br>'
            '<strong>XP für Level {}:</strong> {}<br>'
            '<strong>XP im aktuellen Level:</strong> {} / {}<br>'
            '<strong>Fortschritt:</strong> {}%<br>'
            '</div>'
            '<div style="width: 100%; background-color: #ddd; border-radius: 5px; height: 30px; margin-top: 10px;">'
            '<div style="width: {}%; background-color: #4CD964; height: 100%; border-radius: 5px; line-height: 30px; text-align: center; color: white;">'
            '{}%'
            '</div>'
            '</div>',
            level,
            obj.xp,
            level,
            xp_for_current,
            level + 1,
            xp_for_next,
            xp_current,
            xp_needed,
            percentage,
            percentage,
            percentage
        )
    level_progress_display.short_description = 'Detaillierter Fortschritt'
    
    def xp_info_display(self, obj):
        """Additional XP information"""
        level = obj.get_level()
        return format_html(
            '<table style="width: 100%; border-collapse: collapse;">'
            '<tr><th style="text-align: left; padding: 5px; border-bottom: 1px solid #ddd;">Level</th>'
            '<th style="text-align: right; padding: 5px; border-bottom: 1px solid #ddd;">Benötigte Gesamt-XP</th></tr>'
            '<tr style="background-color: #e8f5e9;"><td style="padding: 5px;"><strong>{}</strong></td><td style="text-align: right; padding: 5px;"><strong>{}</strong></td></tr>'
            '<tr><td style="padding: 5px;">{}</td><td style="text-align: right; padding: 5px;">{}</td></tr>'
            '<tr><td style="padding: 5px;">{}</td><td style="text-align: right; padding: 5px;">{}</td></tr>'
            '</table>',
            level,
            obj.xp,
            level + 1,
            obj.xp_for_level(level + 1),
            level + 2,
            obj.xp_for_level(level + 2)
        )
    xp_info_display.short_description = 'XP Übersicht'
    
    def add_xp_to_users(self, request, queryset):
        """Custom admin action to add XP to selected users"""
        if 'apply' in request.POST:
            form = AddXPForm(request.POST)
            if form.is_valid():
                xp_to_add = form.cleaned_data['xp_to_add']
                
                count = 0
                for level_obj in queryset:
                    # Add XP (level is automatically calculated)
                    level_obj.add_xp(xp_to_add)
                    count += 1
                
                self.message_user(
                    request,
                    f'{xp_to_add} XP wurden {count} User(n) hinzugefügt. Level wird automatisch berechnet.',
                    messages.SUCCESS
                )
                return redirect(request.get_full_path())
        else:
            form = AddXPForm()
        
        return render(
            request,
            'admin/add_xp_form.html',
            context={
                'form': form,
                'users': queryset,
                'title': 'XP hinzufügen (Level-System)',
                'system': 'level'
            }
        )
    
    add_xp_to_users.short_description = "XP zu ausgewählten Users hinzufügen"
    
    def set_xp_for_users(self, request, queryset):
        """Custom admin action to set XP for selected users"""
        if 'apply' in request.POST:
            form = SetXPForm(request.POST)
            if form.is_valid():
                xp_to_set = form.cleaned_data['xp_to_set']
                
                count = 0
                for level_obj in queryset:
                    # Set XP (level is automatically calculated)
                    level_obj.xp = xp_to_set
                    level_obj.save()
                    count += 1
                
                self.message_user(
                    request,
                    f'XP wurde auf {xp_to_set} für {count} User(n) gesetzt. Level wird automatisch berechnet.',
                    messages.SUCCESS
                )
                return redirect(request.get_full_path())
        else:
            form = SetXPForm()
        
        return render(
            request,
            'admin/set_xp_form.html',
            context={
                'form': form,
                'users': queryset,
                'title': 'XP setzen (Level-System)',
                'system': 'level'
            }
        )
    
    set_xp_for_users.short_description = "XP für ausgewählte Users setzen"

