#!/bin/bash
# Obsidian Daily File Organizer
# Automatically creates daily folders and organizes files by date

OBSIDIAN_PATH="/home/rduffy/Documents/Leveling-Life/ConvoCanvas-Vault/01-AI-Conversations"
TODAY=$(date +"%Y-%m-%d")
MONTH=$(date +"%Y-%m")
YEAR=$(date +"%Y")

echo "🗂️ Starting Obsidian file organization for $TODAY..."

# Create directory structure
create_daily_structure() {
    mkdir -p "$OBSIDIAN_PATH/Claude/$YEAR/$MONTH/$TODAY"
    mkdir -p "$OBSIDIAN_PATH/Claude-Code/Sessions/$YEAR/$MONTH/$TODAY"
    mkdir -p "$OBSIDIAN_PATH/Claude-Code/System-Updates/$YEAR/$MONTH"
    echo "✅ Created directory structure for $TODAY"
}

# Move Claude Chat files to daily folders
organize_claude_files() {
    local moved_count=0

    for file in "$OBSIDIAN_PATH"/Claude/2025-*_*.md; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")

            # Extract date from filename: YYYY-MM-DD_HH-MM-SS_...
            if [[ $filename =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})_([0-9]{2}-[0-9]{2}-[0-9]{2})_(.+)$ ]]; then
                file_date="${BASH_REMATCH[1]}"
                file_time="${BASH_REMATCH[2]}"
                file_rest="${BASH_REMATCH[3]}"
                file_year="${file_date:0:4}"
                file_month="${file_date:0:7}"

                # Create target directory if it doesn't exist
                target_dir="$OBSIDIAN_PATH/Claude/$file_year/$file_month/$file_date"
                mkdir -p "$target_dir"

                # New filename: HH-MM-SS_Rest-of-filename
                new_filename="${file_time}_${file_rest}"
                target_file="$target_dir/$new_filename"

                # Move file if not already in correct location
                if [[ "$file" != "$target_file" ]]; then
                    mv "$file" "$target_file"
                    echo "📁 Moved: $filename → $file_date/$new_filename"
                    ((moved_count++))
                fi
            fi
        fi
    done

    echo "✅ Organized $moved_count Claude files"
}

# Move Claude Code files
organize_claude_code_files() {
    local moved_count=0

    for file in "$OBSIDIAN_PATH"/Claude-Code/Sessions/2025-*_*.md; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")

            if [[ $filename =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})_([0-9]{2}-[0-9]{2}-[0-9]{2})_(.+)$ ]]; then
                file_date="${BASH_REMATCH[1]}"
                file_time="${BASH_REMATCH[2]}"
                file_rest="${BASH_REMATCH[3]}"
                file_year="${file_date:0:4}"
                file_month="${file_date:0:7}"

                target_dir="$OBSIDIAN_PATH/Claude-Code/Sessions/$file_year/$file_month/$file_date"
                mkdir -p "$target_dir"

                new_filename="${file_time}_${file_rest}"
                target_file="$target_dir/$new_filename"

                if [[ "$file" != "$target_file" ]]; then
                    mv "$file" "$target_file"
                    echo "🔧 Moved: $filename → Sessions/$file_date/$new_filename"
                    ((moved_count++))
                fi
            fi
        fi
    done

    echo "✅ Organized $moved_count Claude Code files"
}

# Organize system update files
organize_system_updates() {
    local moved_count=0

    for file in "$OBSIDIAN_PATH"/Claude-Code/System-Updates/2025-*_*.md; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")

            if [[ $filename =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})_(.+)$ ]]; then
                file_date="${BASH_REMATCH[1]}"
                file_rest="${BASH_REMATCH[2]}"
                file_year="${file_date:0:4}"
                file_month="${file_date:0:7}"

                target_dir="$OBSIDIAN_PATH/Claude-Code/System-Updates/$file_year/$file_month"
                mkdir -p "$target_dir"

                # Keep system update files with full date prefix
                new_filename="${file_date}_${file_rest}"
                target_file="$target_dir/$new_filename"

                if [[ "$file" != "$target_file" ]]; then
                    mv "$file" "$target_file"
                    echo "📊 Moved: $filename → System-Updates/$file_month/$new_filename"
                    ((moved_count++))
                fi
            fi
        fi
    done

    echo "✅ Organized $moved_count system update files"
}

# Create index files for easy navigation
create_navigation_indices() {
    # Create monthly index for Claude conversations
    claude_month_dir="$OBSIDIAN_PATH/Claude/$YEAR/$MONTH"
    if [[ -d "$claude_month_dir" ]]; then
        index_file="$claude_month_dir/00_${MONTH}_Index.md"

        cat > "$index_file" << EOF
# Claude Conversations - $(date -d "$MONTH-01" +"%B %Y")

**Auto-generated index** | Last updated: $(date)

## Daily Conversations

EOF

        # Add links to daily folders
        for day_dir in "$claude_month_dir"/2025-*; do
            if [[ -d "$day_dir" ]]; then
                day_name=$(basename "$day_dir")
                file_count=$(find "$day_dir" -name "*.md" | wc -l)
                echo "- [[$day_name]] ($file_count files)" >> "$index_file"
            fi
        done

        echo "📋 Created Claude index for $MONTH"
    fi

    # Create monthly index for Claude Code
    code_month_dir="$OBSIDIAN_PATH/Claude-Code/Sessions/$YEAR/$MONTH"
    if [[ -d "$code_month_dir" ]]; then
        index_file="$code_month_dir/00_${MONTH}_Sessions-Index.md"

        cat > "$index_file" << EOF
# Claude Code Sessions - $(date -d "$MONTH-01" +"%B %Y")

**Auto-generated index** | Last updated: $(date)

## Daily Sessions

EOF

        for day_dir in "$code_month_dir"/2025-*; do
            if [[ -d "$day_dir" ]]; then
                day_name=$(basename "$day_dir")
                file_count=$(find "$day_dir" -name "*.md" | wc -l)
                echo "- [[$day_name]] ($file_count sessions)" >> "$index_file"
            fi
        done

        echo "📋 Created Claude Code index for $MONTH"
    fi
}

# Clean up empty directories
cleanup_empty_dirs() {
    find "$OBSIDIAN_PATH" -type d -empty -delete 2>/dev/null
    echo "🧹 Cleaned up empty directories"
}

# Main execution
main() {
    echo "🚀 Obsidian Daily Organizer Starting..."
    echo "📅 Date: $TODAY"
    echo "📂 Path: $OBSIDIAN_PATH"
    echo ""

    create_daily_structure
    organize_claude_files
    organize_claude_code_files
    organize_system_updates
    create_navigation_indices
    cleanup_empty_dirs

    echo ""
    echo "✨ Organization complete!"
    echo "📊 Summary:"
    echo "   - Directory structure: ✅ Created"
    echo "   - Claude files: ✅ Organized"
    echo "   - Claude Code files: ✅ Organized"
    echo "   - System updates: ✅ Organized"
    echo "   - Navigation indices: ✅ Created"
    echo ""
    echo "🎯 Your Obsidian vault is now organized by date!"
}

# Run the organizer
main "$@"