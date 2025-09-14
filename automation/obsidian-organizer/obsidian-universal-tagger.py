#!/usr/bin/env python3
"""
Universal Obsidian Auto-Tagger
Automatically adds YAML frontmatter to ALL markdown files across the entire vault
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

class UniversalObsidianTagger:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.processed_count = 0
        self.skipped_count = 0
        self.error_count = 0

    def extract_file_info(self, file_path):
        """Extract information from various file patterns and locations"""
        filename = file_path.name
        parent_dirs = file_path.parts

        # Initialize default info
        info = {
            'date': None,
            'time': None,
            'source': 'Manual',
            'topic': filename.replace('.md', ''),
            'raw_topic': filename.replace('.md', ''),
            'directory_context': None
        }

        # Determine directory context
        if 'AI-Conversations' in str(file_path):
            if 'Claude-Code' in str(file_path):
                info['source'] = 'Claude Code'
                info['directory_context'] = 'AI-Conversations/Claude-Code'
            elif 'Claude' in str(file_path):
                info['source'] = 'Claude Chat'
                info['directory_context'] = 'AI-Conversations/Claude'
            else:
                info['source'] = 'AI Assistant'
                info['directory_context'] = 'AI-Conversations'
        elif 'Daily Notes' in str(file_path):
            info['source'] = 'Daily Notes'
            info['directory_context'] = 'Daily-Notes'
        elif 'Learning-Log' in str(file_path):
            info['source'] = 'Learning Log'
            if 'Daily-Journal' in str(file_path):
                info['directory_context'] = 'Learning-Log/Daily-Journal'
            elif 'Weekly-Reviews' in str(file_path):
                info['directory_context'] = 'Learning-Log/Weekly-Reviews'
            elif 'Technical-Insights' in str(file_path):
                info['directory_context'] = 'Learning-Log/Technical-Insights'
            else:
                info['directory_context'] = 'Learning-Log'
        elif 'attachments' in str(file_path):
            info['source'] = 'Attachment'
            info['directory_context'] = 'Attachments'

        # Extract date from directory structure
        for part in reversed(parent_dirs):
            if re.match(r'\d{4}-\d{2}-\d{2}', part):
                info['date'] = part
                break

        # Extract date and time from filename patterns
        patterns = [
            # YYYY-MM-DD_HH-MM-SS_Source_Topic pattern
            r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})_(.+?)_(.+)',
            # HH-MM-SS_Source_Topic pattern (organized files)
            r'(\d{2}-\d{2}-\d{2})_(.+?)_(.+)',
            # YYYY-MM-DD-topic pattern
            r'(\d{4}-\d{2}-\d{2})-(.+)',
            # YYYY-MM-DD pattern (daily notes)
            r'(\d{4}-\d{2}-\d{2})',
        ]

        filename_no_ext = filename.replace('.md', '')

        for pattern in patterns:
            match = re.match(pattern, filename_no_ext)
            if match:
                groups = match.groups()

                if len(groups) == 4:  # Full pattern with date, time, source, topic
                    info['date'] = groups[0]
                    info['time'] = groups[1].replace('-', ':')
                    info['source'] = groups[2].replace('-', ' ')
                    info['topic'] = groups[3].replace('....', '').replace('...', '').replace('..', '')
                elif len(groups) == 3 and re.match(r'\d{2}:\d{2}:\d{2}', groups[0].replace('-', ':')):  # Time, source, topic
                    info['time'] = groups[0].replace('-', ':')
                    info['source'] = groups[1].replace('-', ' ')
                    info['topic'] = groups[2].replace('....', '').replace('...', '').replace('..', '')
                elif len(groups) == 3:  # Date, source, topic or similar
                    if re.match(r'\d{4}-\d{2}-\d{2}', groups[0]):
                        info['date'] = groups[0]
                    info['topic'] = ' '.join(groups[1:])
                elif len(groups) == 2:  # Date and topic
                    if re.match(r'\d{4}-\d{2}-\d{2}', groups[0]):
                        info['date'] = groups[0]
                        info['topic'] = groups[1]
                elif len(groups) == 1:  # Just date
                    if re.match(r'\d{4}-\d{2}-\d{2}', groups[0]):
                        info['date'] = groups[0]
                        info['topic'] = 'Daily Note'
                break

        # Use today's date if no date found
        if not info['date']:
            info['date'] = datetime.now().strftime('%Y-%m-%d')

        # Clean up topic
        if info['topic']:
            info['topic'] = info['topic'].replace('_', ' ').replace('-', ' ')

        return info

    def determine_category(self, topic, source, directory_context):
        """Determine category based on topic, source, and location"""
        topic_lower = topic.lower() if topic else ""
        source_lower = source.lower() if source else ""

        # Directory-based categories
        if directory_context:
            if 'Daily-Journal' in directory_context:
                return 'Daily-Journal'
            elif 'Weekly-Reviews' in directory_context:
                return 'Weekly-Review'
            elif 'Technical-Insights' in directory_context:
                return 'Technical-Insight'
            elif 'Daily-Notes' in directory_context:
                return 'Daily-Note'
            elif 'Attachments' in directory_context:
                return 'Attachment'

        # Content-based categories
        if any(word in topic_lower for word in ['config', 'configuration', 'setup', 'install']):
            return 'Configuration'
        elif any(word in topic_lower for word in ['integration', 'connect', 'bridge', 'link']):
            return 'Integration'
        elif any(word in topic_lower for word in ['guide', 'tutorial', 'how-to', 'walkthrough']):
            return 'Guide'
        elif any(word in topic_lower for word in ['review', 'analysis', 'research', 'study']):
            return 'Analysis'
        elif any(word in topic_lower for word in ['troubleshoot', 'debug', 'fix', 'error', 'issue']):
            return 'Troubleshooting'
        elif any(word in topic_lower for word in ['plan', 'planning', 'strategy', 'roadmap']):
            return 'Planning'
        elif any(word in topic_lower for word in ['journal', 'daily', 'log']):
            return 'Journal'
        elif any(word in topic_lower for word in ['note', 'notes']):
            return 'Note'
        elif 'system' in topic_lower and 'update' in topic_lower:
            return 'System-Update'
        else:
            return 'General'

    def generate_tags(self, topic, source, category, directory_context):
        """Generate comprehensive tags"""
        tags = []

        # Source-based tags
        source_lower = source.lower() if source else ""
        if 'claude chat' in source_lower:
            tags.append('claude-chat')
        elif 'claude code' in source_lower:
            tags.append('claude-code')
        elif 'claude' in source_lower:
            tags.append('claude')
        elif 'daily notes' in source_lower:
            tags.append('daily-notes')
        elif 'learning log' in source_lower:
            tags.append('learning-log')

        # Directory context tags
        if directory_context:
            context_tag = directory_context.lower().replace('/', '-').replace(' ', '-')
            tags.append(context_tag)

        # Content-based tags
        topic_lower = topic.lower() if topic else ""
        keywords = {
            'librechat': 'librechat',
            'obsidian': 'obsidian',
            'lm-studio': 'lm-studio',
            'lm studio': 'lm-studio',
            'convocanvas': 'convocanvas',
            'docker': 'docker',
            'web-search': 'web-search',
            'serper': 'serper-api',
            'rag': 'rag',
            'embedding': 'embeddings',
            'github': 'github',
            'reddit': 'reddit',
            'integration': 'integration',
            'configuration': 'configuration',
            'smart connections': 'smart-connections',
            'advanced uri': 'advanced-uri',
            'draw.io': 'drawio',
            'mvp': 'mvp',
            'complete': 'completed-project',
            'python': 'python',
            'javascript': 'javascript',
            'ai': 'artificial-intelligence',
            'automation': 'automation',
            'workflow': 'workflow'
        }

        for keyword, tag in keywords.items():
            if keyword in topic_lower:
                tags.append(tag)

        # Category-based tag
        tags.append(category.lower().replace('-', '_'))

        # Remove duplicates and sort
        return sorted(list(set(tags)))

    def determine_status(self, topic, category):
        """Determine completion status"""
        topic_lower = topic.lower() if topic else ""

        if any(word in topic_lower for word in ['complete', 'finished', 'done', 'mvp']):
            return 'completed'
        elif any(word in topic_lower for word in ['planning', 'strategy', 'roadmap', 'future', 'ideas']):
            return 'planned'
        elif any(word in topic_lower for word in ['progress', 'ongoing', 'update', 'wip']):
            return 'in-progress'
        elif category in ['Daily-Note', 'Daily-Journal', 'Journal']:
            return 'archived'  # Daily entries are archived
        else:
            return 'completed'  # Default for most content

    def determine_priority(self, topic, category, directory_context):
        """Determine priority level"""
        topic_lower = topic.lower() if topic else ""

        if any(word in topic_lower for word in ['critical', 'urgent', 'important']):
            return 'high'
        elif any(word in topic_lower for word in ['minor', 'small', 'quick', 'note']):
            return 'low'
        elif category in ['System-Update', 'Configuration', 'Integration']:
            return 'high'
        elif category in ['Daily-Note', 'Daily-Journal', 'Attachment']:
            return 'low'
        else:
            return 'medium'

    def create_frontmatter(self, file_info):
        """Create comprehensive YAML frontmatter"""
        category = self.determine_category(
            file_info['topic'],
            file_info['source'],
            file_info['directory_context']
        )

        tags = self.generate_tags(
            file_info['topic'],
            file_info['source'],
            category,
            file_info['directory_context']
        )

        status = self.determine_status(file_info['topic'], category)
        priority = self.determine_priority(
            file_info['topic'],
            category,
            file_info['directory_context']
        )

        frontmatter = f"""---
date: {file_info['date']}"""

        if file_info['time']:
            frontmatter += f"\ntime: {file_info['time']}"

        frontmatter += f"""
source: {file_info['source']}
category: {category}"""

        if file_info['directory_context']:
            frontmatter += f"\ncontext: {file_info['directory_context']}"

        frontmatter += f"""
tags: [{', '.join(tags)}]
status: {status}
priority: {priority}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

"""
        return frontmatter

    def process_file(self, file_path):
        """Process a single file"""
        try:
            # Skip system files and directories
            if (file_path.name.startswith('.') or
                file_path.name.startswith('00_') or
                'Index' in file_path.name or
                '.obsidian' in str(file_path) or
                '.smart-env' in str(file_path)):
                self.skipped_count += 1
                return f"⏭️  Skipped (system file): {file_path.name}"

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if already has frontmatter
            if content.startswith('---'):
                self.skipped_count += 1
                return f"⏭️  Skipped (has frontmatter): {file_path.name}"

            # Extract file information
            file_info = self.extract_file_info(file_path)

            # Create frontmatter
            frontmatter = self.create_frontmatter(file_info)
            new_content = frontmatter + content

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.processed_count += 1
            return f"✅ Tagged: {file_path.name} [{file_info['source']}]"

        except Exception as e:
            self.error_count += 1
            return f"❌ Error: {file_path.name} - {str(e)}"

    def run(self):
        """Run the universal tagging process"""
        print("🏷️  Universal Obsidian Auto-Tagger Starting...")
        print(f"📂 Vault Path: {self.vault_path}")
        print("🔍 Processing ALL markdown files in vault...")
        print("")

        # Process all markdown files recursively
        for md_file in self.vault_path.glob('**/*.md'):
            if md_file.is_file():
                result = self.process_file(md_file)
                print(result)

        print("")
        print("📊 Universal Tagging Summary:")
        print(f"   ✅ Files processed: {self.processed_count}")
        print(f"   ⏭️  Files skipped: {self.skipped_count}")
        print(f"   ❌ Errors encountered: {self.error_count}")
        print(f"   📁 Total files checked: {self.processed_count + self.skipped_count + self.error_count}")
        print("")

        if self.processed_count > 0:
            print("✨ Universal auto-tagging complete!")
            print("🎯 Your entire Obsidian vault now has structured metadata!")
        else:
            print("ℹ️  No files were processed. They may already have frontmatter.")

def main():
    vault_path = "/home/rduffy/Documents/Leveling-Life"

    if len(sys.argv) > 1:
        vault_path = sys.argv[1]

    if not os.path.exists(vault_path):
        print(f"❌ Error: Vault path does not exist: {vault_path}")
        sys.exit(1)

    tagger = UniversalObsidianTagger(vault_path)
    tagger.run()

if __name__ == "__main__":
    main()