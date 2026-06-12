import { Component, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { AuditItem, ChatResponse } from '../../models/audit.models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  private api = inject(ApiService);

  items = signal<AuditItem[]>([]);
  selected = signal<AuditItem | null>(null);
  question = '';
  response = signal<ChatResponse | null>(null);
  loading = signal(false);

  criticalCount = computed(() => this.items().filter(x => x.level === 'critical').length);
  avgScore = computed(() =>
    this.items().length
      ? Math.round(this.items().reduce((a, b) => a + b.score, 0) / this.items().length)
      : 0
  );

  constructor() {
    this.refresh();
  }

  refresh(): void {
    this.loading.set(true);
    this.api.getSyntheticData(24).subscribe({
      next: (res) => {
        const rows = res.items as AuditItem[];
        this.items.set(rows);
        this.selected.set(rows[0] || null);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  pick(item: AuditItem): void {
    this.selected.set(item);
  }

  ask(): void {
    const q = this.question.trim();
    if (!q) return;

    this.loading.set(true);
    this.response.set(null);

    this.api.askQuestion(q).subscribe({
      next: (res) => {
        this.response.set(res);
        this.loading.set(false);
      },
      error: () => {
        this.response.set({
          answer: 'Failed to get response from server.',
          context: [],
          type: 'fallback',
          in_scope: false
        });
        this.loading.set(false);
      }
    });
  }
}