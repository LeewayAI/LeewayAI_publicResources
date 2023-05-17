def db_schema
      tables = ActiveRecord::Base.connection.tables.reject { |table_name| ignored?(table_name) }
      tables.map do |table_name|
        { tableName: table_name,
          attributes:
            ActiveRecord::Base.connection.columns(table_name).map { |c| [c.name, c.type] }.to_h
        }
      end
    end

    def ignored?(table_name)
      [ActiveRecord::Base.schema_migrations_table_name, ActiveRecord::Base.internal_metadata_table_name,
       ActiveRecord::SchemaDumper.ignore_tables].flatten.any? do |ignored|
        ignored === remove_prefix_and_suffix(table_name)
      end
    end

    def remove_prefix_and_suffix(table_name)
      prefix = Regexp.escape(Rails.application.config.active_record.table_name_prefix.to_s)
      suffix = Regexp.escape(Rails.application.config.active_record.table_name_suffix.to_s)
      table_name.sub(/\A#{prefix}(.+)#{suffix}\z/, "\\1")
    end