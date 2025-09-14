#!/usr/bin/env python3
"""
Obsidian Auto-Tagger for Organized Files
Automatically adds YAML frontmatter to files in the organized directory structure
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

class ObsidianAutoTaggerOrganized:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.processed_count = 0
        self.skipped_count = 0

    def extract_file_info_from_path(self, file_path):
        """Extract information from file path and organized filename"""
        # Get date from directory structure: .../YYYY/YYYY-MM/YYYY-MM-DD/HH-MM-SS_Source_Topic....md
        path_parts = file_path.parts

        # Find date in path
        date_str = None
        for part in reversed(path_parts):
            if re.match(r'\d{4}-\d{2}-\d{2}', part):
                date_str = part
                break

        if not date_str:
            return None

        filename = file_path.name

        # Pattern for organized files: HH-MM-SS_Source_Topic....md
        time_pattern = r'(\d{2}-\d{2}-\d{2})_(.+?)_(.+)\.md'
        match = re.match(time_pattern, filename)

        if match:
            time, source, topic = match.groups()
            return {
                'date': date_str,
                'time': time.replace('-', ':'),
                'source': source.replace('-', ' '),
                'topic': topic.replace('....', '').replace('...', '').replace('..', ''),
                'raw_topic': topic
            }

        # Alternative pattern for files that might not have been renamed yet
        full_pattern = r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})_(.+?)_(.+)\.md'
        match = re.match(full_pattern, filename)

        if match:
            file_date, time, source, topic = match.groups()
            return {
                'date': file_date,
                'time': time.replace('-', ':'),
                'source': source.replace('-', ' '),
                'topic': topic.replace('....', '').replace('...', '').replace('..', ''),
                'raw_topic': topic
            }

        return None

    def determine_category(self, topic, source):
        """Determine category based on topic content"""
        topic_lower = topic.lower()

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
        elif 'system-changes' in topic_lower or 'update' in topic_lower:
            return 'System-Update'
        else:
            return 'General'

    def generate_tags(self, topic, source, category):
        """Generate relevant tags based on content"""
        tags = []

        # Source-based tags
        source_lower = source.lower()
        if 'claude chat' in source_lower:
            tags.append('claude-chat')
        elif 'claude-code' in source_lower or 'claude code' in source_lower:
            tags.append('claude-code')
        elif 'claude' in source_lower:
            tags.append('claude')

        # Project/technology tags
        topic_lower = topic.lower()
        project_keywords = {
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
            'draw.io': 'drawio'
        }

        for keyword, tag in project_keywords.items():
            if keyword in topic_lower:
                tags.append(tag)

        # Category-based tags
        tags.append(category.lower())

        # Remove duplicates and sort
        return sorted(list(set(tags)))

    def determine_status(self, topic):
        """Determine completion status"""
        topic_lower = topic.lower()

        if any(word in topic_lower for word in ['complete', 'finished', 'done', 'setup', 'guide']):
            return 'completed'
        elif any(word in topic_lower for word in ['planning', 'strategy', 'roadmap', 'future']):
            return 'planned'
        elif any(word in topic_lower for word in ['progress', 'ongoing', 'update']):
            return 'in-progress'
        else:
            return 'completed'  # Default for conversation logs

    def determine_priority(self, topic, category):
        """Determine priority level"""
        topic_lower = topic.lower()

        if any(word in topic_lower for word in ['critical', 'urgent', 'important', 'setup', 'configuration']):
            return 'high'
        elif any(word in topic_lower for word in ['minor', 'small', 'quick', 'note']):
            return 'low'
        elif category in ['System-Update', 'Configuration', 'Integration']:
            return 'high'
        else:
            return 'medium'

    def create_frontmatter(self, file_info):
        """Create YAML frontmatter block"""
        category = self.determine_category(file_info['topic'], file_info['source'])
        tags = self.generate_tags(file_info['topic'], file_info['source'], category)
        status = self.determine_status(file_info['topic'])
        priority = self.determine_priority(file_info['topic'], category)

        frontmatter = f"""---
date: {file_info['date']}
time: {file_info['time']}
source: {file_info['source']}
category: {category}
tags: [{', '.join(tags)}]
status: {status}
priority: {priority}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

"""
        return frontmatter

    def process_file(self, file_path):
        """Process a single file to add frontmatter"""
        try:
            # Skip index files and system files
            if file_path.name.startswith('00_') or 'Index' in file_path.name:
                self.skipped_count += 1
                return f"⏭️  Skipped (index file): {file_path.name}"

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if already has frontmatter
            if content.startswith('---'):
                self.skipped_count += 1
                return f"⏭️  Skipped (already has frontmatter): {file_path.name}"

            # Extract file information
            file_info = self.extract_file_info_from_path(file_path)
            if not file_info:
                self.skipped_count += 1
                return f"⏭️  Skipped (doesn't match pattern): {file_path.name}"

            # Create and add frontmatter
            frontmatter = self.create_frontmatter(file_info)
            new_content = frontmatter + content

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.processed_count += 1
            return f"✅ Tagged: {file_path.name} ({file_info['category']})"

        except Exception as e:
            return f"❌ Error processing {file_path.name}: {str(e)}"

    def process_directory(self, directory_path):
        """Process all markdown files in a directory"""
        results = []

        for md_file in directory_path.glob('**/*.md'):
            if md_file.is_file():
                result = self.process_file(md_file)
                results.append(result)
                print(result)

        return results

    def run(self):
        """Run the auto-tagging process"""
        print("🏷️  Obsidian Auto-Tagger (Organized Files) Starting...")
        print(f"📂 Vault Path: {self.vault_path}")
        print("")

        # Process AI Conversations directory
        conversations_path = self.vault_path / "01-AI-Conversations"
        if conversations_path.exists():
            print("🔍 Processing organized AI Conversations...")
            self.process_directory(conversations_path)
        else:
            print("⚠️  AI Conversations directory not found")

        print("")
        print("📊 Summary:")
        print(f"   - Files processed: {self.processed_count}")
        print(f"   - Files skipped: {self.skipped_count}")
        print(f"   - Total files checked: {self.processed_count + self.skipped_count}")
        print("")

        if self.processed_count > 0:
            print("✨ Auto-tagging complete! Your organized files now have structured metadata.")
        else:
            print("ℹ️  No files were processed. They may already have frontmatter or don't match patterns.")

def main():
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = "/home/rduffy/Documents/Leveling-Life/ConvoCanvas-Vault"

    if not os.path.exists(vault_path):
        print(f"❌ Error: Vault path does not exist: {vault_path}")
        sys.exit(1)

    tagger = ObsidianAutoTaggerOrganized(vault_path)
    tagger.run()

if __name__ == "__main__":
    main()