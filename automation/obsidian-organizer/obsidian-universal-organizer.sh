#!/bin/bash
# Universal Obsidian File Organizer
# Organizes ALL date-based files across the entire Obsidian vault

OBSIDIAN_ROOT="/home/rduffy/Documents/Leveling-Life"
TODAY=$(date +"%Y-%m-%d")
YEAR=$(date +"%Y")
MONTH=$(date +"%Y-%m")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌟 Universal Obsidian Organizer Starting...${NC}"
echo -e "${BLUE}📅 Date: $TODAY${NC}"
echo -e "${BLUE}🏠 Vault Root: $OBSIDIAN_ROOT${NC}"
echo ""

# Statistics
total_moved=0
total_directories_processed=0
total_indices_created=0

# Function to organize files in a directory
organize_directory() {
    local dir="$1"
    local dir_type="$2"
    local moved_count=0

    echo -e "${YELLOW}📂 Processing: $dir${NC}"

    # Find all markdown files with date patterns
    while IFS= read -r -d '' file; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")

            # Match various date patterns
            if [[ $filename =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})(.*)\.md$ ]]; then
                file_date="${BASH_REMATCH[1]}"
                file_rest="${BASH_REMATCH[2]}"
                file_year="${file_date:0:4}"
                file_month="${file_date:0:7}"

                # Create organized directory structure
                target_base="$dir/organized/$file_year/$file_month/$file_date"
                mkdir -p "$target_base"

                # Determine new filename based on rest content
                if [[ "$file_rest" =~ ^_([0-9]{2}-[0-9]{2}-[0-9]{2})_(.+)$ ]]; then
                    # Format: YYYY-MM-DD_HH-MM-SS_Content.md
                    time_part="${BASH_REMATCH[1]}"
                    content_part="${BASH_REMATCH[2]}"
                    new_filename="${time_part}_${content_part}.md"
                elif [[ "$file_rest" =~ ^-(.+)$ ]]; then
                    # Format: YYYY-MM-DD-content.md
                    content_part="${BASH_REMATCH[1]}"
                    new_filename="${content_part}.md"
                elif [[ -z "$file_rest" ]]; then
                    # Format: YYYY-MM-DD.md (daily notes)
                    new_filename="daily-note.md"
                else
                    # Keep rest as is
                    new_filename="${file_rest}.md"
                fi

                target_file="$target_base/$new_filename"

                # Move file if not already in correct location
                if [[ "$file" != "$target_file" ]]; then
                    mv "$file" "$target_file"
                    echo -e "${GREEN}   ✅ Moved: $filename → $file_date/$new_filename${NC}"
                    ((moved_count++))
                fi
            fi
        fi
    done < <(find "$dir" -maxdepth 1 -name "*.md" -type f -print0)

    ((total_moved += moved_count))
    echo -e "${GREEN}   📊 Organized $moved_count files in $dir${NC}"
}

# Function to create navigation index
create_directory_index() {
    local dir="$1"
    local dir_name=$(basename "$dir")
    local organized_dir="$dir/organized"

    if [[ -d "$organized_dir" ]]; then
        local index_file="$organized_dir/00_${dir_name}_Index.md"

        cat > "$index_file" << EOF
# ${dir_name} - Organized Files Index

**Auto-generated** | Last updated: $(date)
**Location**: $dir

## Year-Month Structure

EOF

        # Add links to year/month directories
        for year_dir in "$organized_dir"/*/; do
            if [[ -d "$year_dir" ]]; then
                year_name=$(basename "$year_dir")
                echo "### $year_name" >> "$index_file"
                echo "" >> "$index_file"

                for month_dir in "$year_dir"/*/; do
                    if [[ -d "$month_dir" ]]; then
                        month_name=$(basename "$month_dir")
                        file_count=$(find "$month_dir" -name "*.md" | wc -l)
                        echo "- **$month_name** ($file_count files)" >> "$index_file"

                        # List daily directories
                        for day_dir in "$month_dir"/*/; do
                            if [[ -d "$day_dir" ]]; then
                                day_name=$(basename "$day_dir")
                                day_file_count=$(find "$day_dir" -name "*.md" | wc -l)
                                echo "  - [[$day_name]] ($day_file_count files)" >> "$index_file"
                            fi
                        done
                    fi
                done
                echo "" >> "$index_file"
            fi
        done

        echo -e "${BLUE}📋 Created index: $index_file${NC}"
        ((total_indices_created++))
    fi
}

# Function to process specific directory types
process_ai_conversations() {
    local ai_dir="$OBSIDIAN_ROOT/ConvoCanvas-Vault/01-AI-Conversations"

    if [[ -d "$ai_dir" ]]; then
        echo -e "${YELLOW}🤖 Processing AI Conversations...${NC}"

        # Process any remaining unorganized files in subdirectories
        for subdir in "$ai_dir"/*; do
            if [[ -d "$subdir" && $(basename "$subdir") != "Claude" && $(basename "$subdir") != "Claude-Code" ]]; then
                organize_directory "$subdir" "ai-conversation"
                create_directory_index "$subdir"
            fi
        done
        ((total_directories_processed++))
    fi
}

process_daily_notes() {
    local daily_dir="$OBSIDIAN_ROOT/Daily Notes"

    if [[ -d "$daily_dir" ]]; then
        echo -e "${YELLOW}📅 Processing Daily Notes...${NC}"
        organize_directory "$daily_dir" "daily-notes"
        create_directory_index "$daily_dir"
        ((total_directories_processed++))
    fi
}

process_learning_log() {
    local learning_dir="$OBSIDIAN_ROOT/ConvoCanvas-Vault/03-Learning-Log"

    if [[ -d "$learning_dir" ]]; then
        echo -e "${YELLOW}📚 Processing Learning Log...${NC}"

        # Process each subdirectory
        for subdir in "$learning_dir"/*; do
            if [[ -d "$subdir" ]]; then
                subdir_name=$(basename "$subdir")
                echo -e "${YELLOW}  📂 Processing $subdir_name...${NC}"
                organize_directory "$subdir" "learning-log"
                create_directory_index "$subdir"
            fi
        done
        ((total_directories_processed++))
    fi
}

process_attachments() {
    local attachments_dir="$OBSIDIAN_ROOT/attachments"

    if [[ -d "$attachments_dir" ]]; then
        echo -e "${YELLOW}📎 Processing Attachments...${NC}"
        organize_directory "$attachments_dir" "attachments"
        create_directory_index "$attachments_dir"
        ((total_directories_processed++))
    fi
}

process_any_remaining() {
    echo -e "${YELLOW}🔍 Scanning for remaining date-based files...${NC}"

    # Find any remaining date-based files anywhere in the vault
    while IFS= read -r -d '' file; do
        dir=$(dirname "$file")

        # Skip already organized directories
        if [[ "$dir" == *"/organized/"* ]]; then
            continue
        fi

        # Skip hidden directories and system files
        if [[ "$dir" == *"/.obsidian"* || "$dir" == *"/.smart-env"* ]]; then
            continue
        fi

        # Process the parent directory
        organize_directory "$dir" "general"
        create_directory_index "$dir"

    done < <(find "$OBSIDIAN_ROOT" -name "*[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*.md" -type f -print0)
}

# Function to clean up empty directories
cleanup_empty_dirs() {
    echo -e "${YELLOW}🧹 Cleaning up empty directories...${NC}"
    find "$OBSIDIAN_ROOT" -type d -empty -delete 2>/dev/null
    echo -e "${GREEN}✅ Cleanup complete${NC}"
}

# Function to create master index
create_master_index() {
    local master_index="$OBSIDIAN_ROOT/ConvoCanvas-Vault/00_Master-Organization-Index.md"

    cat > "$master_index" << EOF
# Master Organization Index

**Auto-generated** | Last updated: $(date)
**Universal Organizer Run**: $TODAY

## Organized Directories

This index shows all directories that have been organized with date-based file structures.

EOF

    # Scan for organized directories
    while IFS= read -r -d '' organized_dir; do
        parent_dir=$(dirname "$organized_dir")
        parent_name=$(basename "$parent_dir")
        relative_path=${organized_dir#$OBSIDIAN_ROOT/}

        echo "### $parent_name" >> "$master_index"
        echo "**Path**: \`$relative_path\`" >> "$master_index"

        # Count files in organized structure
        file_count=$(find "$organized_dir" -name "*.md" -not -name "00_*" | wc -l)
        echo "**Files**: $file_count organized files" >> "$master_index"
        echo "" >> "$master_index"

        # Link to directory index if it exists
        for index_file in "$organized_dir"/00_*_Index.md; do
            if [[ -f "$index_file" ]]; then
                index_name=$(basename "$index_file" .md)
                echo "📋 [[${index_name}|View Index]]" >> "$master_index"
                echo "" >> "$master_index"
                break
            fi
        done

    done < <(find "$OBSIDIAN_ROOT" -name "organized" -type d -print0)

    echo -e "${BLUE}📊 Created master index: $master_index${NC}"
    ((total_indices_created++))
}

# Main execution
main() {
    echo -e "${BLUE}🚀 Starting universal organization...${NC}"
    echo ""

    # Process different directory types
    process_ai_conversations
    process_daily_notes
    process_learning_log
    process_attachments
    process_any_remaining

    # Create master index
    create_master_index

    # Cleanup
    cleanup_empty_dirs

    echo ""
    echo -e "${GREEN}✨ Universal organization complete!${NC}"
    echo -e "${GREEN}📊 Final Summary:${NC}"
    echo -e "${GREEN}   - Total files moved: $total_moved${NC}"
    echo -e "${GREEN}   - Directories processed: $total_directories_processed${NC}"
    echo -e "${GREEN}   - Navigation indices created: $total_indices_created${NC}"
    echo ""
    echo -e "${BLUE}🎯 Your entire Obsidian vault is now organized by date!${NC}"
    echo -e "${BLUE}📋 Check the Master Organization Index for navigation.${NC}"
}

# Run the universal organizer
main "$@"